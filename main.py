"""
Main application entry point for NDA Agent
"""

import logging
from agents.nda_agent import NDAAgent, Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main application entry point"""
    print("🤖 NDA Agent - PandaDoc Integration")
    print("=" * 50)
    
    try:
        # Initialize configuration
        config = Config()
        
        # Initialize NDA Agent
        logger.info("Initializing NDA Agent...")
        nda_agent = NDAAgent(config)
        
        # Perform health check
        print("\n🔍 Performing health check...")
        health_status = nda_agent.health_check()
        
        print(f"Overall Status: {health_status['overall'].upper()}")
        print("\nComponent Status:")
        for component, status in health_status['components'].items():
            status_emoji = "✅" if status['status'] == 'healthy' else "⚠️" if status['status'] == 'disabled' else "❌"
            print(f"  {status_emoji} {component.title()}: {status['status']} - {status['details']}")
        
        # Get NDA statistics
        print("\n📊 NDA Statistics:")
        stats = nda_agent.get_nda_statistics()
        
        if "error" not in stats:
            print(f"  • Total Documents: {stats.get('total_documents', 0)}")
            print(f"  • Documents Sent: {stats.get('documents_sent', 0)}")
            print(f"  • Documents Signed: {stats.get('documents_signed', 0)}")
            print(f"  • Pending Signatures: {stats.get('pending_signatures', 0)}")
            
            if stats.get('recent_activity'):
                print("\n📋 Recent Activity:")
                for activity in stats['recent_activity'][:3]:  # Show last 3
                    print(f"  • {activity.get('timestamp', 'N/A')}: {activity.get('action', 'N/A').title()} - {activity.get('template_name', 'N/A')}")
        else:
            print(f"  ❌ Error fetching statistics: {stats['error']}")
        
        # Check for pending signatures
        print("\n⏳ Checking pending signatures...")
        pending = nda_agent.check_pending_signatures()
        
        if "error" not in pending:
            pending_count = pending.get('pending_count', 0)
            if pending_count > 0:
                print(f"  ⚠️  {pending_count} documents awaiting signature")
                for doc in pending.get('pending_documents', [])[:3]:  # Show first 3
                    print(f"    • {doc.get('name', 'Unknown')} (ID: {doc.get('id', 'N/A')})")
            else:
                print("  ✅ No pending signatures")
        else:
            print(f"  ❌ Error checking pending signatures: {pending['error']}")
        
        # Interactive options
        print("\n🚀 Available Actions:")
        print("  1. Start interactive chat")
        print("  2. Run example commands")
        print("  3. Show agent capabilities")
        print("  4. Exit")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-4): ").strip()
                
                if choice == "1":
                    print("\n🗣️  Starting interactive chat...")
                    nda_agent.chat()
                    break
                
                elif choice == "2":
                    print("\n📝 Running example commands...")
                    run_examples(nda_agent)
                    break
                
                elif choice == "3":
                    print("\n🔧 Agent Capabilities:")
                    show_capabilities()
                    break
                
                elif choice == "4":
                    print("👋 Goodbye!")
                    break
                
                else:
                    print("❌ Invalid choice. Please enter 1-4.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
    
    except Exception as e:
        logger.error(f"Error in main application: {e}")
        print(f"❌ Error: {e}")


def run_examples(nda_agent: NDAAgent):
    """Run example commands"""
    examples = [
        "List my PandaDoc templates",
        "Get my NDA statistics",
        "Check for pending signatures",
        "What can you help me with?"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. Example: '{example}'")
        print("-" * 30)
        
        try:
            response = nda_agent.run(example)
            print(f"Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")


def show_capabilities():
    """Show agent capabilities"""
    capabilities = [
        "📋 Template Management",
        "  • List available templates",
        "  • Get template details",
        "  • Create documents from templates",
        "",
        "📄 Document Management", 
        "  • Create NDA workflows",
        "  • Send documents for signature",
        "  • Check document status",
        "  • Track document progress",
        "",
        "📊 Analytics & Reporting",
        "  • Generate NDA statistics",
        "  • Track pending signatures",
        "  • Log activities to Google Sheets",
        "  • Send daily summaries",
        "",
        "🔔 Notifications",
        "  • Email notifications for key events",
        "  • Document status updates",
        "  • Daily activity summaries",
        "",
        "🤖 Natural Language Interface",
        "  • Ask questions in plain English",
        "  • Get help with NDA processes",
        "  • Automated workflow execution"
    ]
    
    for capability in capabilities:
        print(capability)


if __name__ == "__main__":
    main()
