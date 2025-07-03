from agno.agent import Agent
from agno_agent.panda_tools import PandaDocTool, create_pandadoc_functions
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    # Get API key from environment variable or replace with your actual key
    API_KEY = os.getenv("PANDADOC_API_KEY", "your_actual_api_key")
    
    if API_KEY == "your_actual_api_key":
        print("⚠️  Please set your PandaDoc API key in the PANDADOC_API_KEY environment variable")
        print("   or replace 'your_actual_api_key' with your actual API key in main.py")
        return
    
    # Initialize PandaDoc tool
    panda_tool = PandaDocTool(api_key=API_KEY)
    
    # Create agno functions
    pandadoc_functions = create_pandadoc_functions(API_KEY)
    
    # Initialize Agno agent with the functions
    agent = Agent(
        name="PandaDoc Agent",
        description="An agent that can interact with PandaDoc API to manage templates and documents",
        tools=pandadoc_functions,
        markdown=True,
        show_tool_calls=True
    )
    
    print("🐼 PandaDoc API Integration with Agno Framework")
    print("=" * 50)
    
    # List templates
    print("\n📋 Fetching available templates...")
    templates = panda_tool.list_templates()
    
    if "error" in templates:
        print(f"❌ Error: {templates['error']}")
        return
    
    template_results = templates.get("results", [])
    
    if not template_results:
        print("📝 No templates found in your PandaDoc account.")
        return
    
    print(f"\n✅ Found {len(template_results)} templates:")
    print("-" * 30)
    
    for i, template in enumerate(template_results, 1):
        name = template.get('name', 'Unknown')
        template_id = template.get('id', 'N/A')
        created_date = template.get('date_created', 'N/A')
        
        print(f"{i}. {name}")
        print(f"   ID: {template_id}")
        print(f"   Created: {created_date}")
        print()
    
    # Example: Get details for the first template
    if template_results:
        first_template = template_results[0]
        template_id = first_template.get('id')
        
        print(f"\n🔍 Getting details for template: {first_template.get('name')}")
        details = panda_tool.get_template_details(template_id)
        
        if "error" not in details:
            print("✅ Template details retrieved successfully!")
            print(f"   Fields: {len(details.get('fields', []))}")
            print(f"   Roles: {len(details.get('roles', []))}")
        else:
            print(f"❌ Error getting template details: {details['error']}")
    
    # Test agent interaction
    print("\n🤖 Testing agent interaction...")
    print("You can now interact with the agent using: agent.run('list my templates')")
    print("Or try: agent.run('tell me about my first template')")


if __name__ == "__main__":
    main()
