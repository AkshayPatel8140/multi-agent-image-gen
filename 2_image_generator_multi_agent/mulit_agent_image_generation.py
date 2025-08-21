# AI Image Generator using Two Agents
# This script demonstrates how two AI agents work together:
# 1) Prompt Engineer: turns your idea into a detailed image description
# 2) Image Generator: creates the actual image using OpenAI's API

# Setup instructions:
# python -m venv .venv
# source .venv/bin/activate  # On Mac/Linux
# pip install langgraph langchain openai
# export OPENAI_API_KEY=your_key_here

from __future__ import annotations

import os
import requests
from datetime import datetime
from typing import Annotated, Literal

from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.types import Command
from openai import OpenAI


# Configuration - you can change these models
CHAT_MODEL = "openai:gpt-4.1-mini"
IMAGE_MODEL = "dall-e-3"


# ============================
# Image Generation Function
# ============================
def generate_image_with_openai(prompt: str, size: str = "1024x1024") -> str:
    """Creates an image using OpenAI's API and saves it locally"""

    client = OpenAI()

    # Generate the image
    result = client.images.generate(
        model=IMAGE_MODEL,
        prompt=prompt,
        size=size,
        n=1,
    )

    # DALL-E 3 returns URLs, not base64 data
    image_url = result.data[0].url

    # Download the image from the URL
    response = requests.get(image_url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Create folder and save with timestamp
    os.makedirs("generated_images", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join("generated_images", f"image_{timestamp}.png")

    # Save the downloaded image
    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path


# ============================
# Graph State Structure
# ============================
class MessagesState(TypedDict):
    messages: Annotated[list, add_messages]


# ============================
# Agent Instructions
# ============================
PROMPT_ENGINEER_INSTRUCTIONS = (
    "Act as a world-class prompt engineer for text-to-image models. "
    "Given a user idea, produce a single polished prompt that is concrete, visual, and style-aware. "
    "Include subject, scene, composition, lighting, lens, color palette, and quality tags. "
    "Avoid copyrighted terms and disallowed content. "
    "Output exactly one line starting with: FINAL PROMPT: "
)

IMAGE_AGENT_SYS = (
    "Act as an image-generation operator. "
    "Input will be a single line starting with 'FINAL PROMPT:'. "
    "Call the image tool with that prompt. "
    "When done, respond with exactly one line starting with 'FINAL ANSWER:' followed by the local file path."
)

# ============================
# Initialize AI Model
# ============================
llm = init_chat_model(CHAT_MODEL)


# ============================
# Helper Function
# ============================
def check_if_finished(last_message: BaseMessage, default_next: str) -> str:
    """Check if we're done or should continue"""
    content = getattr(last_message, "content", "")
    if isinstance(content, str) and content.startswith("FINAL ANSWER:"):
        return END
    return default_next


# ============================
# Agent Functions
# ============================
def prompt_engineer_agent(state: MessagesState) -> Command[Literal["image_node", END]]:
    """First agent: turns user idea into detailed image description"""

    # Prepare messages for the AI
    messages = [SystemMessage(content=PROMPT_ENGINEER_INSTRUCTIONS), *state["messages"]]
    ai_response = llm.invoke(messages)

    # Format the response
    response_text = ai_response.content.strip()
    if "FINAL PROMPT:" not in response_text:
        response_text = "FINAL PROMPT: " + response_text.replace("\n", " ").strip()

    # Add response to conversation and move to next agent
    updated_messages = state["messages"] + [
        AIMessage(content=response_text, name="prompt_engineer")
    ]
    # goto = _route(AIMessage(content=text), "image_node")
    return Command(update={"messages": updated_messages}, goto="image_node")


def image_generator_agent(state: MessagesState) -> Command[Literal[END, "prompt_node"]]:
    """Second agent: creates the actual image using OpenAI Images API after reading the engineered prompt."""

    detailed_prompt = None

    # Search through messages in reverse order to find the most recent prompt
    for message in reversed(state["messages"]):
        # Extract the text content from each message
        content = getattr(message, "content", "")
        # Check if this message contains the engineered prompt
        if isinstance(content, str) and content.startswith("FINAL PROMPT:"):
            detailed_prompt = content.replace("FINAL PROMPT:", "").strip()
            break

    # If no prompt found, go back to the first agent
    if not detailed_prompt:
        return Command(update={}, goto="prompt_node")

    # Generate the image
    image_file_path = generate_image_with_openai(detailed_prompt, size="1024x1024")
    response = f"FINAL ANSWER: {image_file_path}"

    # Add response and finish
    updated_messages = state["messages"] + [
        AIMessage(content=response, name="image_agent")
    ]
    return Command(update={"messages": updated_messages}, goto=END)


# ============================
# Build the Agent Graph
# ============================
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("prompt_node", prompt_engineer_agent)
graph_builder.add_node("image_node", image_generator_agent)

graph_builder.add_edge(START, "prompt_node")

graph = graph_builder.compile()


# ============================
# Main Program
# ============================
if __name__ == "__main__":
    print("🎨 AI Image Generator - Two Agent System")
    print("=" * 50)
    print("Example idea:")
    print(
        "A cozy steampunk library interior with warm light and brass, isometric view, ultra-detailed"
    )

    user_idea = input("\n💡 Your idea: ").strip()

    # Run the agent system
    final_image_path = None
    for event in graph.stream(
        {"messages": [HumanMessage(content=user_idea)]}, stream_mode="values"
    ):
        last_message = event["messages"][-1]
        message_text = getattr(last_message, "content", "")
        print("🤖 Agent:", message_text)

        if isinstance(message_text, str) and message_text.startswith("FINAL ANSWER:"):
            final_image_path = message_text.replace("FINAL ANSWER:", "").strip()
            break

    if final_image_path:
        print(f"\n✅ Image saved to: {final_image_path}")
        print("🎉 Your AI-generated image is ready!")
