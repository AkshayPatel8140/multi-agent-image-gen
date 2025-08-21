"""
Brand-Aware AI Image Generator
-------------------------------
Multi-agent pipeline that creates perfectly branded images:
1. Loads brand knowledge (colors, voice, dos/donts, logo variants, typography, style)
2. Engineers brand-aware image prompts that follow your style guidelines
3. Generates base images using OpenAI's DALL-E 3 API
4. Composites brand logos exactly as specified without distortion

Perfect for demonstrations of AI-powered brand consistency!
"""

# Setup instructions:
# python -m venv .venv
# source .venv/bin/activate  # On Mac/Linux
# .venv\Scripts\activate     # On Windows
# pip install langgraph langchain openai pillow numpy requests
# export OPENAI_API_KEY=your_key_here

# Usage example:
# python brand_image_agent.py --company acme --idea "A futuristic office space with green plants" --size 1024x1024 --position top-right

from __future__ import annotations
import os, json
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, Dict, Literal, Optional
from typing_extensions import TypedDict

import numpy as np
from PIL import Image
from openai import OpenAI
from io import BytesIO
import requests

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.types import Command


# ============================
# Configuration
# ============================
CHAT_MODEL = "openai:gpt-4.1-mini"
IMAGE_MODEL = "dall-e-3"  # Updated to DALL-E 3 for better quality
KB_DIR = "brand_kb"
OUTPUT_DIR = "generated_brand_image"


# ============================
# Brand Knowledge Base Loader
# ============================
@dataclass
class BrandKBItem:
    """
    Container for one brand's complete metadata.
    This structure ensures type safety and comprehensive brand information.
    """

    key: str
    display_name: str
    brand_colors_hex: list
    voice: str
    visual_style: str
    dos: list
    donts: list
    logo_variants: Dict[str, str]
    default_logo_preference: str
    default_logo_position: str
    typography: str  # New field for font guidelines
    image_style: str  # New field for overall visual approach


def load_kb() -> Dict[str, BrandKBItem]:
    """
    Load brand metadata from brand_kb.json and instantiate BrandKBItem objects keyed by lowercase brand key.
    """
    path = os.path.join(KB_DIR, "brand_kb.json")

    # UTF-8 ensures consistent decoding for non-ASCII brand names and notes
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    out: Dict[str, BrandKBItem] = {}
    for k, v in data.items():
        out[k.lower()] = BrandKBItem(
            key=k.lower(),
            display_name=v.get("display_name", k),
            brand_colors_hex=v.get("brand_colors_hex", []),
            voice=v.get("voice", ""),
            visual_style=v.get("visual_style", ""),
            dos=v.get("dos", []),
            donts=v.get("donts", []),
            logo_variants=v.get("logo_variants", {}),
            default_logo_preference=v.get("default_logo_preference", "light"),
            default_logo_position=v.get("default_logo_position", "top-right"),
            typography=v.get("typography", ""),
            image_style=v.get("image_style", ""),
        )
    return out


KB = load_kb()
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================
# OpenAI Image Generator
# ============================
def openai_image_generator(prompt: str, size="1024x1024") -> Image.Image:
    """
    Generate an image using OpenAI's DALL-E 3 API.
    Args:
        prompt: Text description for the image model
        size: Image dimensions (e.g., '1024x1024', '1792x1024', '1024x1792')
    Returns: PIL.Image.Image in memory
    """
    client = OpenAI()

    try:
        # Generate image using DALL-E 3
        result = client.images.generate(
            model=IMAGE_MODEL, prompt=prompt, size=size, n=1, quality="standard"
        )

        # DALL-E 3 returns URLs, not base64 data
        image_url = result.data[0].url

        # Download the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Convert to PIL Image
        return Image.open(BytesIO(response.content))

    except Exception as e:
        print(f"❌ Error generating image: {e}")
        raise ValueError(f"Failed to generate image: {e}")


# ============================
# Image Processing Services
# ============================


def average_luminance(img: Image.Image) -> float:
    """
    Compute a rough average luminance (0-255)(GrayScale) of the image. Used to decide light vs dark logo for best contrast.
    """
    small = img.convert("L").resize((32, 32))
    return float(np.array(small).mean())


def choose_logo_variant(brand: BrandKBItem, base_img: Image.Image) -> str:
    """
    Pick 'light' or 'dark' logo variant based on base image luminance, falling back to brand defaults.
    """
    if base_img is None:
        pref = brand.default_logo_preference
        return brand.logo_variants.get(pref) or list(brand.logo_variants.values())[0]

    lum = average_luminance(base_img)

    if lum >= 128:
        return (
            brand.logo_variants.get("dark")
            or brand.logo_variants.get("light")
            or list(brand.logo_variants.values())[0]
        )
    else:
        return (
            brand.logo_variants.get("light")
            or brand.logo_variants.get("dark")
            or list(brand.logo_variants.values())[0]
        )


def place_logo(
    base_img: Image.Image,
    logo_img: Image.Image,
    position: str,
    max_width_ratio: float = 0.25,
    padding_ratio: float = 0.03,
) -> Image.Image:
    """
    Overlay the logo onto the base image at a given position.
    Preserves aspect ratio; never recolors or rotates the logo.
    Args:
        base_img: background image;
        logo_img: transparent PNG preferred;
        position: top-left/top-center/top-right/bottom-left/bottom-center/bottom-right;
        max_width_ratio: cap for logo width as a fraction of image width;
        padding_ratio: margin from edges.
    Note: Image.LANCZOS is a high-quality downsampling filter used when resizing the logo to avoid aliasing or blur.
    """

    bw, bh = base_img.size

    # max with of the logo
    max_w = int(bw * max_width_ratio)
    lw, lh = logo_img.size

    # Scale down if needed
    if lw > max_w:
        scale = max_w / float(lw)
        new_w = max(1, int(lw * scale))
        new_h = max(1, int(lh * scale))
        logo_img = logo_img.resize((new_w, new_h), Image.LANCZOS)
        lw, lh = logo_img.size

    # padding
    pad = int(min(bw, bh) * padding_ratio)

    # coordinates
    pos = position.lower()
    if pos == "top-left":
        x, y = pad, pad
    elif pos == "top-center":
        x, y = (bw - lw) // 2, pad
    elif pos == "top-right":
        x, y = bw - lw - pad, pad
    elif pos == "bottom-left":
        x, y = pad, bh - lh - pad
    elif pos == "bottom-center":
        x, y = (bw - lw) // 2, bh - lh - pad
    else:
        # bottom-right by default
        x, y = bw - lw - pad, bh - lh - pad

    # ensure RGBA
    if base_img.mode != "RGBA":
        base_img = base_img.convert("RGBA")
    if logo_img.mode != "RGBA":
        logo_img = logo_img.convert("RGBA")

    base = base_img.copy()
    base.alpha_composite(logo_img, (x, y))
    return base.convert("RGB")


def save_image(img: Image.Image, prefix: str) -> str:
    """
    Persist a PIL Image as PNG under OUTPUT_DIR with a timestamped filename and return its path.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_DIR, f"{prefix}_{ts}.png")
    img.save(path, format="PNG")
    return path


# ============================
# Shared Graph State
# ============================
class State(TypedDict):
    messages: Annotated[list, add_messages]
    company_key: str  # "acme"
    size: str  # "1024x1024"
    preferred_position: Optional[str]  # "Can override brand default"


# ============================
# System Prompts
# ============================
# System instruction for the prompt-engineering agent.
PROMPT_ENGINEER_SYS = (
    "Act as a world-class brand-aware image prompt engineer. "
    "Use ALL the provided brand details faithfully, including: "
    "voice, visual_style, dos and donts, brand_colors_hex, typography, and image_style. "
    "Construct a single polished image prompt that perfectly matches the brand's aesthetic and the described idea. "
    "Do not include the word 'logo' in the prompt - the logo will be composited later. "
    "Make the prompt specific, visual, and aligned with the brand's personality. "
    "Output exactly one line starting with 'FINAL PROMPT: '."
)


def brand_context_text(b: BrandKBItem) -> str:
    """
    Render the brand KB item into a comprehensive text block for the LLM.
    Includes all brand guidelines for better AI understanding.
    """
    return (
        f"Brand: {b.display_name}\n"
        f"Voice: {b.voice}\n"
        f"Visual style: {b.visual_style}\n"
        f"Brand colors: {', '.join(b.brand_colors_hex)}\n"
        f"Do: {', '.join(b.dos)}\n"
        f"Do not: {', '.join(b.donts)}\n"
        f"Typography: {b.typography}\n"
        f"Image style: {b.image_style}\n"
    )


# =========================
# Define LLM
# =========================
llm = init_chat_model(CHAT_MODEL)


# =========================
# Nodes
# =========================
def brand_node(state: State) -> Command[Literal["prompt_node"]]:
    """
    Lookup the brand in the KB and append a [BRAND_CONTEXT] message so later nodes can incorporate brand details.
    """
    company = state["company_key"].lower()
    if company not in KB:
        raise ValueError(
            f"Unknown company key: '{company}'. Add it to {os.path.join(KB_DIR, 'brand_kb.json')}."
        )
    brand_data = KB[company]

    # Inject a brand summary message so downstream node can use it
    brand_msg = AIMessage(
        content=f"[BRAND_CONTEXT]\n{brand_context_text(brand_data)}", name="brand_kb"
    )
    return Command(
        update={"messages": state["messages"] + [brand_msg]}, goto="prompt_node"
    )


def prompt_node(state: State) -> Command[Literal["image_node", END]]:
    """
    Produce a single-line engineered prompt using the brand context and the user's idea.
    """
    brand_text = ""
    for m in reversed(state["messages"]):
        if getattr(m, "name", "") == "brand_kb":
            brand_text = getattr(m, "content", "")
            break

    msgs = [
        SystemMessage(content=PROMPT_ENGINEER_SYS),
        AIMessage(content=brand_text),
        *state["messages"],
    ]
    ai = llm.invoke(msgs)
    text = ai.content.strip().replace("\n", " ")
    if not text.startswith("FINAL PROMPT:"):
        text = "FINAL PROMPT: " + text.strip()

    return Command(
        update={
            "messages": state["messages"]
            + [AIMessage(content=text, name="prompt_engineer")]
        },
        goto="image_node",
    )


def image_node(state: State) -> Command[Literal["compose_node"]]:
    """
    Generate the base image from the engineered prompt and stash its path as a [BASE_IMAGE] message.
    """
    final_prompt = None
    for m in reversed(state["messages"]):
        c = getattr(m, "content", "")
        if isinstance(c, str) and c.startswith("FINAL PROMPT:"):
            final_prompt = c.replace("FINAL PROMPT:", "").strip()
            break
    if not final_prompt:
        raise ValueError("Missing Final PROMPT From the prompt_node.")

    # Generate base Image
    base = openai_image_generator(final_prompt, size=state.get("size", "1024x1024"))

    # Stash base path for the inspection
    base_path = save_image(base, prefix="base")
    msg = AIMessage(content=f"[BASE_IMAGE] {base_path}", name="image_generator")
    return Command(update={"messages": state["messages"] + [msg]}, goto="compose_node")


def compose_node(state: State) -> Command[Literal[END]]:
    """
    Load the base image, pick the best logo variant, composite it at the configured position, and return the final file path.
    """
    company = state["company_key"].lower()
    brand = KB[company]

    # Load the last base image
    base_path = None
    for m in reversed(state["messages"]):
        c = getattr(m, "content", "")
        if isinstance(c, str) and c.startswith("[BASE_IMAGE]"):
            base_path = c.replace("[BASE_IMAGE]", "").strip()
            break

    if not base_path:
        raise ValueError("Base image Path missing.")

    base_img = Image.open(base_path)

    logo_path = choose_logo_variant(brand, base_img)
    full_logo_path = (
        os.path.join(KB_DIR, logo_path)
        if not logo_path.startswith(KB_DIR)
        else logo_path
    )

    if not os.path.exists(full_logo_path):
        raise ValueError(f"Logo file not found: {full_logo_path}")

    logo_img = Image.open(full_logo_path)
    position = state.get("preferred_position", brand.default_logo_position)
    final_img = place_logo(base_img, logo_img, position=position)

    out_path = save_image(final_img, prefix=f"{company}_final")
    out_msg = AIMessage(content=f"FINAL ANSWER: {out_path}", name="composer")
    return Command(update={"messages": state["messages"] + [out_msg]}, goto=END)


# =========================
# Graph
# =========================
builder = StateGraph(State)
builder.add_node("brand_node", brand_node)
builder.add_node("prompt_node", prompt_node)
builder.add_node("image_node", image_node)
builder.add_node("compose_node", compose_node)

builder.add_edge(START, "brand_node")
builder.add_edge("brand_node", "prompt_node")
builder.add_edge("prompt_node", "image_node")
builder.add_edge("image_node", "compose_node")

graph = builder.compile()


# ============================
# Main Entry Point
# ============================
# Command-line interface to run brand-aware image generation
if __name__ == "__main__":
    import argparse

    print("🎨 Brand-Aware AI Image Generator")
    print("=" * 50)
    print("This system creates perfectly branded images using AI agents!")
    print()

    parser = argparse.ArgumentParser(
        description="Generate brand-consistent images with AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            python brand_image_agent.py --company acme --idea "A futuristic office space with green plants"
            python brand_image_agent.py --company red&white --idea "Students learning in a modern classroom" --size 1792x1024
            python brand_image_agent.py --company techflow --idea "Team collaboration in a tech startup" --position top-left
        """,
    )

    parser.add_argument(
        "--company",
        required=True,
        choices=["acme", "red&white", "techflow", "creative_studio", "eco_green"],
        help="Brand to use for image generation",
    )
    parser.add_argument("--idea", required=True, help="Your image idea description")
    parser.add_argument(
        "--size",
        default="1024x1024",
        choices=["1024x1024", "1792x1024", "1024x1792"],
        help="Image dimensions",
    )
    parser.add_argument(
        "--position",
        default=None,
        choices=[
            "top-left",
            "top-center",
            "top-right",
            "bottom-left",
            "bottom-center",
            "bottom-right",
            "center",
        ],
        help="Logo position (overrides brand default)",
    )

    args = parser.parse_args()

    print(f"🏢 Brand: {args.company}")
    print(f"💡 Idea: {args.idea}")
    print(f"📐 Size: {args.size}")
    if args.position:
        print(f"📍 Logo Position: {args.position}")
    print()

    # Initialize the agent system
    state = {
        "messages": [HumanMessage(content=args.idea)],
        "company_key": args.company,
        "size": args.size,
        "preferred_position": args.position,
    }

    print("🚀 Starting AI agent pipeline...")
    print("=" * 40)

    final_path = None
    step_count = 0

    for event in graph.stream(state, stream_mode="values"):
        step_count += 1
        last = event["messages"][-1]
        text = getattr(last, "content", "")

        # Show progress for each agent step
        if step_count == 1:
            print("🤖 Agent 1: Loading brand guidelines...")
        elif step_count == 2:
            print("🤖 Agent 2: Engineering brand-aware prompt...")
        elif step_count == 3:
            print("🤖 Agent 3: Generating base image...")
        elif step_count == 4:
            print("🤖 Agent 4: Compositing logo...")

        print(f"   {text[:100]}{'...' if len(text) > 100 else ''}")

        if isinstance(text, str) and text.startswith("FINAL ANSWER:"):
            final_path = text.replace("FINAL ANSWER:", "").strip()
            break

    print("=" * 40)
    if final_path:
        print(f"✅ Success! Your branded image is ready at:")
        print(f"📁 {final_path}")
        print("\n🎉 The AI agents have created a perfectly branded image for you!")
    else:
        print("❌ Something went wrong during image generation.")
        print("Please check your OpenAI API key and try again.")
