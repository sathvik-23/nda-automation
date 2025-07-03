#!/usr/bin/env python3
"""
Interactive script to demonstrate PandaDoc Agent capabilities
"""

import os
import sys
from dotenv import load_dotenv
from agno.agent import Agent
from agno_agent.panda_tools import create_pandadoc_functions

# Load environment variables
load_dotenv()


def main():
    # Get API key
    API_KEY = os.getenv("PANDADOC_API_KEY")
    
    if not API_KEY or API_KEY == "your_actual_api_key_here":
        print("❌ API key not found. Please set PANDADOC_API_KEY in your .env file")
        return
    
    print("🤖 PandaDoc Agent - Interactive Demo")
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
    
    print("✅ Agent initialized successfully!")
    print("\nTry these example commands:")
    print("- 'list my templates'")
    print("- 'tell me about my first template'")
    print("- 'how many templates do I have?'")
    print("- 'what can you help me with?'")
    print("\nType 'quit' to exit\n")
    
    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nAgent: ", end="")
            response = agent.run(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
