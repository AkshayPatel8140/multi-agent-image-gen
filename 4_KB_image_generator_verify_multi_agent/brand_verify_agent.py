"""
Brand-Aware AI Image Generator with Verification
-----------------------------------------------
Multi-agent pipeline that:
1. Loads brand knowledge (colors, voice, dos/donts, logo variants, typography, style)
2. Engineers brand-aware image prompts that follow your style guidelines
3. Generates base images using OpenAI's DALL-E 3 API
4. Composites brand logos exactly as specified without distortion
5. VERIFIES the generated image matches brand criteria and outputs results

Perfect for demonstrations of AI-powered brand consistency with verification!
"""

# Setup instructions:
# python -m venv .venv
# source .venv/bin/activate  # On Mac/Linux
# .venv\Scripts\activate     # On Windows
# pip install langgraph langchain openai pillow numpy requests
# export OPENAI_API_KEY=your_key_here

from __future__ import annotations
import os
import json
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Annotated, Dict, Literal, Optional, List, Tuple, Any, TypedDict

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
IMAGE_MODEL = "dall-e-3"  # Using DALL-E 3 for better quality
KB_DIR = "brand_kb"
OUTPUT_DIR = "generated_brand_image"
VERIFICATION_DIR = "verification_results"


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
    typography: str
    image_style: str


def load_kb() -> Dict[str, BrandKBItem]:
    """
    Load brand metadata from brand_kb.json and instantiate BrandKBItem objects.
    """
    path = os.path.join(KB_DIR, "brand_kb.json")

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
os.makedirs(VERIFICATION_DIR, exist_ok=True)


# ============================
# OpenAI Image Generator
# ============================
def openai_image_generator(prompt: str, size: str = "1024x1024") -> Image.Image:
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
    Compute a rough average luminance (0-255) of the image.
    Used to decide light vs dark logo for best contrast.
    """
    small = img.convert("L").resize((32, 32))
    return float(np.array(small).mean())


def choose_logo_variant(brand: BrandKBItem, base_img: Image.Image) -> str:
    """
    Pick 'light' or 'dark' logo variant based on base image luminance.
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
    """
    bw, bh = base_img.size

    # Max width of the logo
    max_w = int(bw * max_width_ratio)
    lw, lh = logo_img.size

    # Scale down if needed
    if lw > max_w:
        scale = max_w / float(lw)
        new_w = max(1, int(lw * scale))
        new_h = max(1, int(lh * scale))
        logo_img = logo_img.resize((new_w, new_h), Image.LANCZOS)
        lw, lh = logo_img.size

    # Padding
    pad = int(min(bw, bh) * padding_ratio)

    # Coordinates based on position
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
    elif pos == "center":
        x, y = (bw - lw) // 2, (bh - lh) // 2
    else:
        # bottom-right by default
        x, y = bw - lw - pad, bh - lh - pad

    # Ensure RGBA
    if base_img.mode != "RGBA":
        base_img = base_img.convert("RGBA")
    if logo_img.mode != "RGBA":
        logo_img = logo_img.convert("RGBA")

    base = base_img.copy()
    base.alpha_composite(logo_img, (x, y))
    return base.convert("RGB")


def save_image(img: Image.Image, prefix: str) -> str:
    """
    Persist a PIL Image as PNG under OUTPUT_DIR with a timestamped filename.
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(OUTPUT_DIR, f"{prefix}_{ts}.png")
    img.save(path, format="PNG")
    return path


# ============================
# Brand Verification System
# ============================
def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.strip().lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in [0, 2, 4])


def dominant_colors(image: Image.Image, k: int = 5) -> List[Tuple[int, int, int]]:
    """
    Extract dominant colors from image using simple downsampling.
    Good enough for a quick palette proximity check.
    """
    small = image.copy().resize((64, 64))
    arr = np.array(small).reshape(-1, 3)

    # Count unique colors
    colors, counts = np.unique(arr, axis=0, return_counts=True)
    order = np.argsort(counts)[::-1]
    colors_sorted = [tuple(map(int, colors[i])) for i in order[:k]]
    return colors_sorted


def color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Calculate Euclidean distance between two RGB colors."""
    return float(np.linalg.norm(np.array(c1) - np.array(c2)))


def check_palette_compliance(
    image: Image.Image, brand: BrandKBItem, threshold: float = 80.0
) -> Dict[str, Any]:
    """
    Check if the image's dominant colors match the brand palette.
    Returns compliance report with distances and overall result.
    """
    dom = dominant_colors(image, k=5)
    palette = [hex_to_rgb(hx) for hx in brand.brand_colors_hex]

    distances = []
    for d in dom:
        closest = min(color_distance(d, p) for p in palette) if palette else 0.0
        distances.append({"dominant_color": d, "closest_distance": round(closest, 2)})

    ok = (
        all(item["closest_distance"] <= threshold for item in distances)
        if palette
        else True
    )

    return {
        "compliant": ok,
        "threshold": threshold,
        "dominant_to_palette_distances": distances,
        "brand_colors": brand.brand_colors_hex,
    }


def check_style_compliance(prompt: str, brand: BrandKBItem) -> Dict[str, Any]:
    """
    Check if the generated prompt follows brand style guidelines.
    """
    prompt_lower = prompt.lower()

    # Check for forbidden terms
    forbidden_found = []
    for term in brand.donts:
        if term.lower() in prompt_lower:
            forbidden_found.append(term)

    # Check for required style elements
    style_elements_present = []
    style_keywords = [
        "modern",
        "clean",
        "professional",
        "innovative",
        "friendly",
        "trustworthy",
    ]
    for keyword in style_keywords:
        if keyword.lower() in prompt_lower:
            style_elements_present.append(keyword)

    # Check if prompt mentions brand colors
    colors_mentioned = []
    for color in brand.brand_colors_hex:
        color_name = color.lower()
        if color_name in prompt_lower or color in prompt_lower:
            colors_mentioned.append(color)

    return {
        "forbidden_terms_found": forbidden_found,
        "style_elements_present": style_elements_present,
        "brand_colors_mentioned": colors_mentioned,
        "overall_style_compliant": len(forbidden_found) == 0
        and len(style_elements_present) > 0,
    }


def run_brand_verification(
    prompt: str, image: Image.Image, brand: BrandKBItem
) -> Dict[str, Any]:
    """
    Run comprehensive brand verification checks.
    Returns detailed compliance report.
    """
    palette_check = check_palette_compliance(image, brand)
    style_check = check_style_compliance(prompt, brand)

    # Overall compliance score
    overall_compliant = (
        palette_check["compliant"] and style_check["overall_style_compliant"]
    )

    return {
        "overall_compliant": overall_compliant,
        "palette_compliance": palette_check,
        "style_compliance": style_check,
        "verification_timestamp": datetime.now(timezone.utc).isoformat(),
        "brand_name": brand.display_name,
        "brand_key": brand.key,
    }


def save_verification_report(
    verification_result: Dict[str, Any], image_path: str, prompt: str, state: State
) -> str:
    """
    Save verification report to JSON file.
    """
    company = state["company_key"].lower()
    brand = KB[company]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create comprehensive report
    report = {
        "verification_report": verification_result,
        "user_input": {
            "user_company": company,
            "user_idea": state["messages"][0].content,
            "user_size": state.get("size", "1024x1024"),
            "user_position": state.get("preferred_position", brand.default_logo_position),
        },
        "generation_details": {
            "prompt": prompt,
            "image_path": image_path,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "image_hash": hashlib.sha256(open(image_path, "rb").read()).hexdigest(),
        },
        "summary": {
            "brand_compliant": verification_result["overall_compliant"],
            "palette_compliant": verification_result["palette_compliance"]["compliant"],
            "style_compliant": verification_result["style_compliance"]["overall_style_compliant"],
        },
    }

    # Save to verification directory
    report_path = os.path.join(
        VERIFICATION_DIR, f"verification_report_{timestamp}.json"
    )
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report_path


# ============================
# Graph State Structure
# ============================
class State(TypedDict):
    messages: Annotated[list, add_messages]
    company_key: str  # "acme"
    size: str  # "1024x1024"
    preferred_position: Optional[str]  # Can override brand default


# ============================
# System Prompts
# ============================
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


# ============================
# Initialize AI Model
# ============================
llm = init_chat_model(CHAT_MODEL)


# ============================
# Agent Functions
# ============================
def brand_node(state: State) -> Command[Literal["prompt_node"]]:
    """
    Lookup the brand in the KB and append a [BRAND_CONTEXT] message.
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
    Generate the base image from the engineered prompt and stash its path.
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


def compose_node(state: State) -> Command[Literal["verify_node"]]:
    """
    Load the base image, pick the best logo variant, composite it at the configured position.
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
    out_msg = AIMessage(content=f"[FINAL_IMAGE] {out_path}", name="composer")
    return Command(
        update={"messages": state["messages"] + [out_msg]}, goto="verify_node"
    )


def verify_node(state: State) -> Command[Literal[END]]:
    """
    Run brand verification on the generated image and save the report.
    """
    company = state["company_key"].lower()
    brand = KB[company]

    # Get the final image path
    final_image_path = None
    for m in reversed(state["messages"]):
        c = getattr(m, "content", "")
        if isinstance(c, str) and c.startswith("[FINAL_IMAGE]"):
            final_image_path = c.replace("[FINAL_IMAGE]", "").strip()
            break

    if not final_image_path:
        raise ValueError("Final image path missing.")

    # Get the engineered prompt
    final_prompt = None
    for m in reversed(state["messages"]):
        c = getattr(m, "content", "")
        if isinstance(c, str) and c.startswith("FINAL PROMPT:"):
            final_prompt = c.replace("FINAL PROMPT:", "").strip()
            break

    # Load the final image for verification
    final_img = Image.open(final_image_path)

    # Run brand verification
    verification_result = run_brand_verification(final_prompt, final_img, brand)

    # Save verification report
    report_path = save_verification_report(
        verification_result, final_image_path, final_prompt, state
    )

    # Create final response
    final_response = f"FINAL ANSWER: {final_image_path}|{report_path}|{verification_result['overall_compliant']}"
    out_msg = AIMessage(content=final_response, name="verifier")

    return Command(update={"messages": state["messages"] + [out_msg]}, goto=END)


# ============================
# Build the Agent Graph
# ============================
builder = StateGraph(State)
builder.add_node("brand_node", brand_node)
builder.add_node("prompt_node", prompt_node)
builder.add_node("image_node", image_node)
builder.add_node("compose_node", compose_node)
builder.add_node("verify_node", verify_node)

builder.add_edge(START, "brand_node")
builder.add_edge("brand_node", "prompt_node")
builder.add_edge("prompt_node", "image_node")
builder.add_edge("image_node", "compose_node")
builder.add_edge("compose_node", "verify_node")

graph = builder.compile()


# ============================
# Main Entry Point
# ============================
if __name__ == "__main__":
    import argparse

    print("🎨 Brand-Aware AI Image Generator with Verification")
    print("=" * 60)
    print("This system creates perfectly branded images and verifies compliance!")
    print()

    parser = argparse.ArgumentParser(
        description="Generate brand-consistent images with AI agents and verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python brand_verify_agent.py --company acme --idea "A futuristic office space with green plants"
  python brand_verify_agent.py --company red&white --idea "Students learning in a modern classroom" --size 1792x1024
  python brand_verify_agent.py --company techflow --idea "Team collaboration meeting" --position top-left
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

    print("🚀 Starting AI agent pipeline with verification...")
    print("=" * 60)

    final_image_path = None
    verification_report_path = None
    brand_compliant = False
    step_count = 0

    for event in graph.stream(state, stream_mode="values"):
        step_count += 1
        last_message = event["messages"][-1]
        message_text = getattr(last_message, "content", "")

        # Show progress for each agent step
        if step_count == 1:
            print("🤖 Agent 1: Loading brand guidelines...")
        elif step_count == 2:
            print("🤖 Agent 2: Engineering brand-aware prompt...")
        elif step_count == 3:
            print("🤖 Agent 3: Generating base image...")
        elif step_count == 4:
            print("🤖 Agent 4: Compositing logo...")
        elif step_count == 5:
            print("🤖 Agent 5: Verifying brand compliance...")

        print(f"   {message_text[:100]}{'...' if len(message_text) > 100 else ''}")

        if isinstance(message_text, str) and message_text.startswith("FINAL ANSWER:"):
            parts = message_text.replace("FINAL ANSWER:", "").strip().split("|")
            if len(parts) >= 3:
                final_image_path = parts[0]
                verification_report_path = parts[1]
                brand_compliant = parts[2].lower() == "true"
            break

    print("=" * 60)
    if final_image_path and verification_report_path:
        print(f"✅ Success! Your branded image is ready at:")
        print(f"📁 {final_image_path}")
        print(f"📊 Verification report: {verification_report_path}")
        print(
            f"🎯 Brand Compliance: {'✅ COMPLIANT' if brand_compliant else '❌ NOT COMPLIANT'}"
        )
        print("\n🎉 The AI agents have created and verified your branded image!")

        if not brand_compliant:
            print("\n⚠️  Note: The image doesn't fully meet brand guidelines.")
            print(
                "   Check the verification report for details on what needs improvement."
            )
    else:
        print("❌ Something went wrong during image generation or verification.")
        print("Please check your OpenAI API key and try again.")
