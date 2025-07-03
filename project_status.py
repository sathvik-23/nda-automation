#!/usr/bin/env python3
"""
Project Status Summary
"""

import os
from datetime import datetime

def show_status():
    """Show current project status"""
    print("🎉 PandaDoc + Agno Integration - Project Status")
    print("=" * 50)
    
    # Check files
    files_to_check = [
        ".env",
        ".env.example", 
        "main.py",
        "test_connection.py",
        "interactive_demo.py",
        "usage_examples.py",
        "agno_agent/panda_tools.py",
        "agno_agent/__init__.py",
        "requirements.txt",
        "README.md"
    ]
    
    print("📁 File Status:")
    for file in files_to_check:
        path = f"/Users/sathvik/aix/nda-agno/{file}"
        if os.path.exists(path):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file}")
    
    print("\n🔧 Available Scripts:")
    print("  • main.py - Basic template listing and agent setup")
    print("  • test_connection.py - Test API connectivity")
    print("  • interactive_demo.py - Interactive chat with agent")
    print("  • usage_examples.py - Programmatic usage examples")
    print("  • setup.sh - Automated setup")
    
    print("\n🚀 Next Steps:")
    print("  1. Run: python test_connection.py")
    print("  2. Run: python main.py")
    print("  3. Try: python interactive_demo.py")
    print("  4. Explore: python usage_examples.py")
    
    print("\n🔑 API Key Status:")
    api_key = os.getenv("PANDADOC_API_KEY")
    if api_key and api_key != "your_actual_api_key_here":
        print("  ✅ API key configured")
    else:
        print("  ⚠️  API key not configured (edit .env file)")
    
    print(f"\n📅 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    show_status()
