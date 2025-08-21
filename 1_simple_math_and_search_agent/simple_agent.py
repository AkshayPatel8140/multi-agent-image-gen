"""
Simple Math and Search Agent using LangChain and LangGraph
========================================================

This module demonstrates how to build a basic AI agent that can:
1. Perform mathematical calculations safely
2. Search the web using DuckDuckGo
3. Make intelligent decisions about which tools to use

The agent is built using LangGraph's state management and LangChain's tool system,
showcasing a simple but powerful architecture for tool-using AI agents.

Perfect for:
- Learning AI agent development
- Understanding LangChain and LangGraph
- Building foundation for more complex agents
- Educational and research purposes
"""

import os
import ast
import operator as op
from typing import Annotated, List
from typing_extensions import TypedDict

# Load environment variables (for API keys)
from dotenv import load_dotenv
load_dotenv()

# LangChain and LangGraph imports
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun


# =============================================================================
# TOOL DEFINITIONS
# =============================================================================

@tool
def calculator(expression: str) -> str:
    """
    Safely evaluate basic arithmetic expressions.
    
    This tool uses Python's AST (Abstract Syntax Tree) to safely parse and evaluate
    mathematical expressions, preventing code injection attacks.
    
    Args:
        expression (str): Mathematical expression as a string (e.g., "2*(3+4)/5")
        
    Returns:
        str: Result of the calculation as a string
        
    Raises:
        ValueError: If the expression contains disallowed operations or non-numeric values
        
    Example:
        >>> calculator("2*(3+4)/5")
        '2.8'
    """
    
    # Define allowed mathematical operations for security
    allowed_ops = {
        ast.Add: op.add,        # Addition (+)
        ast.Sub: op.sub,        # Subtraction (-)
        ast.Mult: op.mul,       # Multiplication (*)
        ast.Div: op.truediv,    # Division (/)
        ast.Pow: op.pow,        # Exponentiation (**)
        ast.USub: op.neg,       # Unary minus (-x)
        ast.UAdd: op.pos,       # Unary plus (+x)
    }

    def _eval(node):
        """Recursively evaluate AST nodes safely."""
        if isinstance(node, ast.Constant):
            # Handle Python >= 3.8 (modern approach)
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numeric values are allowed in expressions")
        if isinstance(node, ast.BinOp):
            # Handle binary operations (e.g., 2 + 3)
            return allowed_ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):
            # Handle unary operations (e.g., -5, +3)
            return allowed_ops[type(node.op)](_eval(node.operand))
        raise ValueError("Expression contains disallowed operations")

    try:
        # Parse the expression into an AST
        tree = ast.parse(expression, mode="eval")
        result = _eval(tree.body)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


# Initialize the search tool (no API key required)
search_tool = DuckDuckGoSearchRun()

# Compile the list of available tools
tools = [search_tool, calculator]


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

class State(TypedDict):
    """
    Defines the state structure for the LangGraph agent.
    
    The state contains a list of messages that represents the conversation
    history between the user and the agent.
    """
    messages: Annotated[List[BaseMessage], add_messages]


# =============================================================================
# LANGUAGE MODEL CONFIGURATION
# =============================================================================

def initialize_language_model():
    """
    Initialize and configure the language model with tools.
    
    This function sets up the LLM and binds the available tools to it,
    allowing the model to understand when and how to use each tool.
    
    Returns:
        The configured language model with bound tools
    """
    
    # Initialize the chat model
    # You can easily switch between different providers:
    # - OpenAI: "openai:gpt-4o-mini" or "openai:gpt-4"
    # - Anthropic: "anthropic:claude-3-5-sonnet-20241022"
    # - Google: "google_genai:gemini-1.5-flash"
    # - Local: "ollama:llama3.1" (requires Ollama installation)
    
    llm = init_chat_model("openai:gpt-4o-mini")
    
    # Bind the tools to the language model
    # This allows the LLM to understand what tools are available
    # and when to use them based on the user's request
    llm_with_tools = llm.bind_tools(tools)
    
    return llm_with_tools


# =============================================================================
# AGENT NODES
# =============================================================================

def chatbot_node(state: State):
    """
    Main chatbot node that processes user messages and decides on actions.
    
    This node receives the current state (conversation history) and
    uses the language model to generate a response or decide to use tools.
    
    Args:
        state (State): Current conversation state
        
    Returns:
        dict: Updated state with the model's response
    """
    llm_with_tools = initialize_language_model()
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# =============================================================================
# GRAPH CONSTRUCTION
# =============================================================================

def build_agent_graph():
    """
    Construct the LangGraph workflow for the agent.
    
    This function creates a directed graph that defines how the agent
    processes requests and decides between generating responses or using tools.
    
    The flow is:
    1. START → chatbot (process user input)
    2. chatbot → tools (if tools are needed)
    3. tools → chatbot (process tool results)
    4. chatbot → END (when response is complete)
    
    Returns:
        Compiled LangGraph workflow
    """
    
    # Create a new state graph
    graph_builder = StateGraph(State)
    
    # Add the main nodes
    graph_builder.add_node("chatbot", chatbot_node)
    graph_builder.add_node("tools", ToolNode(tools=tools))
    
    # Define the flow
    graph_builder.add_edge(START, "chatbot")
    
    # Add conditional edge from chatbot to tools
    # The tools_condition function decides whether to use tools or end
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    
    # Add edge from tools back to chatbot
    graph_builder.add_edge("tools", "chatbot")
    
    # Compile the graph for execution
    return graph_builder.compile()


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def run_interactive_session():
    """
    Run an interactive chat session with the agent.
    
    This function provides a command-line interface for users to interact
    with the agent, demonstrating its capabilities in real-time.
    """
    
    print("🤖 Simple Math and Search Agent")
    print("=" * 40)
    print("This agent can help you with:")
    print("• Mathematical calculations (e.g., 'What is (2.5+7)/3?')")
    print("• Web searches (e.g., 'Search for information about LangGraph')")
    print("• General questions and conversations")
    print("\nType 'quit', 'exit', or 'q' to end the session")
    print("Press Ctrl+C to interrupt at any time")
    print("-" * 40)
    
    # Build and compile the agent graph
    graph = build_agent_graph()
    
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in {"q", "quit", "exit"}:
                print("👋 Goodbye! Thanks for trying the agent!")
                break
            
            if not user_input:
                continue
            
            print("🤖 Agent: ", end="", flush=True)
            
            # Process the user input through the agent graph
            # Stream the results for real-time feedback
            for event in graph.stream(
                {"messages": [HumanMessage(content=user_input)]}, 
                stream_mode="values",
                recursion_limit=1000
            ):
                # Get the last message from the event
                last_message = event["messages"][-1]
                
                # Extract and display the content
                content = getattr(last_message, "content", str(last_message))
                if content:
                    print("\n" + content + "\n")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set.")
        print("   Please set your OpenAI API key to use this agent.")
        print("   Example: export OPENAI_API_KEY=sk-...")
        print()
    
    # Run the interactive session
    run_interactive_session()
