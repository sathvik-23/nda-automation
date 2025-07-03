#!/usr/bin/env python3
"""
Usage examples for PandaDoc Agent
"""

import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno_agent.panda_tools import create_pandadoc_functions

# Load environment variables
load_dotenv()


def run_examples():
    """Run example interactions with the PandaDoc Agent"""
    
    # Get API key
    API_KEY = os.getenv("PANDADOC_API_KEY")
    
    if not API_KEY or API_KEY == "your_actual_api_key_here":
        print("❌ API key not found. Please set PANDADOC_API_KEY in your .env file")
        return
    
    print("📚 PandaDoc Agent - Usage Examples")
    print("=" * 40)
    
    # Create agent
    pandadoc_functions = create_pandadoc_functions(API_KEY)
    agent = Agent(
        name="PandaDoc Assistant",
        description="I can help you manage your PandaDoc templates and documents",
        tools=pandadoc_functions,
        markdown=True,
        show_tool_calls=True
    )
    
    examples = [
        "List all my templates",
        "How many templates do I have?",
        "Tell me about my templates",
        "What can you help me with?"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Example: '{example}'")
        print("-" * 30)
        
        try:
            response = agent.run(example)
            print(f"Agent Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()


if __name__ == "__main__":
    run_examples()
