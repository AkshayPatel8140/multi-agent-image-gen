#!/usr/bin/env python3
"""
Demo Script for Simple Math and Search Agent
===========================================

This script demonstrates the agent's capabilities with predefined examples.
Perfect for showcasing the agent in presentations.

Run with: python demo.py
"""

import os
import time
from simple_agent import build_agent_graph, HumanMessage

def print_demo_header():
    """Print a nice header for the demo."""
    print("🎬 Simple Math and Search Agent - Demo Mode")
    print("=" * 50)
    print("This demo will showcase the agent's capabilities with")
    print("predefined examples. Sit back and watch the magic! 🪄")
    print()

def run_demo_example(graph, question, description, delay=2):
    """
    Run a single demo example.
    
    Args:
        graph: The compiled agent graph
        question: The question to ask
        description: Description of what this example demonstrates
        delay: Delay between examples in seconds
    """
    print(f"\n🔍 Example: {description}")
    print("-" * 40)
    print(f"👤 Question: {question}")
    print("🤖 Agent: ", end="", flush=True)
    
    # Process the question through the agent
    try:
        for event in graph.stream(
            {"messages": [HumanMessage(content=question)]}, 
            stream_mode="values"
        ):
            last_message = event["messages"][-1]
            content = getattr(last_message, "content", str(last_message))
            if content:
                print(content)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Wait before next example
    time.sleep(delay)

def run_interactive_demo():
    """Run the interactive demo with predefined examples."""
    print_demo_header()
    
    # Build the agent graph
    print("🔧 Building agent graph...")
    graph = build_agent_graph()
    print("✅ Agent ready!")
    
    # Demo examples
    examples = [
        {
            "question": "What is (15 + 27) * 3?",
            "description": "Mathematical Calculation",
            "delay": 3
        },
        {
            "question": "Search for information about LangGraph and what it's used for",
            "description": "Web Search Capability",
            "delay": 4
        },
        {
            "question": "Calculate 2^8 and then search for how many bytes that represents in computer science",
            "description": "Combined Math and Search",
            "delay": 5
        },
        {
            "question": "What is the current population of Tokyo, and what percentage of Japan's total population does that represent?",
            "description": "Complex Multi-Step Reasoning",
            "delay": 6
        },
        {
            "question": "Tell me a joke about artificial intelligence",
            "description": "General Conversation",
            "delay": 3
        }
    ]
    
    print(f"\n📋 Running {len(examples)} demo examples...")
    print("Each example will show different capabilities of the agent.")
    
    for i, example in enumerate(examples, 1):
        print(f"\n🎯 Example {i}/{len(examples)}")
        run_demo_example(
            graph, 
            example["question"], 
            example["description"], 
            example["delay"]
        )
    
    print("\n🎉 Demo complete!")
    print("=" * 50)
    print("The agent successfully demonstrated:")
    print("✅ Mathematical calculations")
    print("✅ Web search capabilities")
    print("✅ Tool selection and decision making")
    print("✅ Multi-step reasoning")
    print("✅ Natural language processing")
    print("\n🚀 Ready to try your own questions? Run: python simple_agent.py")

def main():
    """Main demo function."""
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key before running the demo.")
        print("Example: export OPENAI_API_KEY=sk-your-api-key-here")
        return
    
    try:
        run_interactive_demo()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        print("Please check your setup and try again.")

if __name__ == "__main__":
    main()
