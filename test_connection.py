#!/usr/bin/env python3
"""
Test script to validate PandaDoc API connection
"""

import os
import sys
from dotenv import load_dotenv
from agno_agent.panda_tools import PandaDocTool

# Load environment variables
load_dotenv()

def test_connection():
    """Test the PandaDoc API connection"""
    print("🧪 Testing PandaDoc API Connection")
    print("=" * 40)
    
    # Get API key
    api_key = os.getenv("PANDADOC_API_KEY")
    
    if not api_key or api_key == "your_actual_api_key_here":
        print("❌ API key not found or not set properly")
        print("Please set PANDADOC_API_KEY in your .env file")
        return False
    
    # Initialize tool
    panda_tool = PandaDocTool(api_key=api_key)
    
    # Test API connection
    print("🔗 Testing API connection...")
    templates = panda_tool.list_templates()
    
    if "error" in templates:
        print(f"❌ Connection failed: {templates['error']}")
        return False
    
    template_count = len(templates.get("results", []))
    print(f"✅ Connection successful! Found {template_count} templates")
    
    return True

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
