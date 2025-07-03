#!/usr/bin/env python3
"""
Interactive demo script for NDA Agent
"""

import logging
from agents.nda_agent import NDAAgent, Config

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Reduce logging noise in interactive mode
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main interactive demo"""
    print("🤖 NDA Agent - Interactive Demo")
    print("=" * 40)
    
    try:
        # Initialize agent
        print("🔄 Initializing NDA Agent...")
        config = Config()
        nda_agent = NDAAgent(config)
        
        # Quick health check
        health_status = nda_agent.health_check()
        print(f"✅ Agent Status: {health_status['overall'].upper()}")
        
        # Show example commands
        print("\n💡 Try these example commands:")
        examples = [
            "List my PandaDoc templates",
            "How many templates do I have?",
            "Get my NDA statistics",
            "Check for pending signatures",
            "What can you help me with?",
            "Create an NDA workflow",
            "Send daily summary",
            "Show me recent activity"
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"  {i}. {example}")
        
        print("\n🎯 Advanced Commands:")
        advanced_examples = [
            "Create an NDA for John Doe at Acme Corp with email john@acme.com using template [template_id]",
            "Log a manual action for document [doc_id]",
            "Check the health of all components"
        ]
        
        for example in advanced_examples:
            print(f"  • {example}")
        
        print("\n" + "=" * 40)
        print("💬 Interactive Chat - Type your questions or commands")
        print("Type 'help' for more options, 'quit' to exit")
        print("=" * 40)
        
        # Interactive chat loop
        while True:
            try:
                user_input = input("\n🗣️  You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    show_help()
                    continue
                
                if user_input.lower() == 'examples':
                    show_examples()
                    continue
                
                if user_input.lower() == 'health':
                    show_health(nda_agent)
                    continue
                
                if not user_input:
                    continue
                
                print("\n🤖 Agent: ", end="")
                response = nda_agent.run(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                logger.error(f"Error in interactive demo: {e}")
    
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        logger.error(f"Failed to initialize agent: {e}")


def show_help():
    """Show help information"""
    print("\n📚 NDA Agent Help")
    print("=" * 30)
    print("Available commands:")
    print("  • help - Show this help message")
    print("  • examples - Show example queries")
    print("  • health - Show component health status")
    print("  • quit/exit/q - Exit the chat")
    print("\nCapabilities:")
    print("  • Document Management - Create, send, track NDAs")
    print("  • Template Management - List and manage templates")
    print("  • Statistics - View NDA statistics and activity")
    print("  • Notifications - Email alerts and summaries")
    print("  • Workflow Automation - Complete NDA processes")


def show_examples():
    """Show example queries"""
    print("\n📝 Example Queries")
    print("=" * 30)
    
    categories = {
        "Template Management": [
            "List my templates",
            "Show template details for [template_id]",
            "How many templates do I have?"
        ],
        "Document Management": [
            "Create a new NDA document",
            "Check document status for [doc_id]",
            "Send document [doc_id] for signature"
        ],
        "Statistics & Reporting": [
            "Get my NDA statistics",
            "Show recent activity",
            "Check for pending signatures"
        ],
        "Workflow Automation": [
            "Create an NDA workflow for [name] at [company]",
            "Send daily summary",
            "Log a manual action"
        ]
    }
    
    for category, examples in categories.items():
        print(f"\n{category}:")
        for example in examples:
            print(f"  • {example}")


def show_health(nda_agent):
    """Show component health status"""
    print("\n🏥 Component Health Status")
    print("=" * 35)
    
    health_status = nda_agent.health_check()
    
    print(f"Overall Status: {health_status['overall'].upper()}")
    print("\nComponents:")
    
    for component, status in health_status['components'].items():
        status_emoji = "✅" if status['status'] == 'healthy' else "⚠️" if status['status'] in ['disabled', 'unavailable'] else "❌"
        print(f"  {status_emoji} {component.title()}: {status['status']}")
        if status['status'] != 'healthy':
            print(f"    Details: {status['details']}")


if __name__ == "__main__":
    main()
