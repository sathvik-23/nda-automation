#!/usr/bin/env python3
"""
Test script to validate NDA Agent components
"""

import sys
import logging
from agents.nda_agent import NDAAgent, Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_agent_components():
    """Test all NDA Agent components"""
    print("🧪 Testing NDA Agent Components")
    print("=" * 40)
    
    try:
        # Test configuration
        print("1. Testing Configuration...")
        config = Config()
        print(f"   ✅ Configuration loaded successfully")
        print(f"   • Agent Name: {config.agent_name}")
        print(f"   • Debug Mode: {config.debug_mode}")
        
        # Test NDA Agent initialization
        print("\n2. Testing NDA Agent Initialization...")
        nda_agent = NDAAgent(config)
        print("   ✅ NDA Agent initialized successfully")
        
        # Test health check
        print("\n3. Testing Health Check...")
        health_status = nda_agent.health_check()
        print(f"   Overall Status: {health_status['overall'].upper()}")
        
        all_healthy = True
        for component, status in health_status['components'].items():
            status_emoji = "✅" if status['status'] == 'healthy' else "⚠️" if status['status'] in ['disabled', 'unavailable'] else "❌"
            print(f"   {status_emoji} {component.title()}: {status['status']}")
            if status['status'] == 'unhealthy':
                all_healthy = False
                print(f"      Error: {status['details']}")
        
        # Test basic functionality
        print("\n4. Testing Basic Functionality...")
        
        # Test template listing
        try:
            response = nda_agent.run("List my templates")
            print("   ✅ Template listing works")
        except Exception as e:
            print(f"   ❌ Template listing failed: {e}")
            all_healthy = False
        
        # Test statistics
        try:
            stats = nda_agent.get_nda_statistics()
            if "error" not in stats:
                print("   ✅ Statistics retrieval works")
            else:
                print(f"   ⚠️  Statistics retrieval has issues: {stats['error']}")
        except Exception as e:
            print(f"   ❌ Statistics retrieval failed: {e}")
        
        # Test pending signatures check
        try:
            pending = nda_agent.check_pending_signatures()
            if "error" not in pending:
                print("   ✅ Pending signatures check works")
            else:
                print(f"   ⚠️  Pending signatures check has issues: {pending['error']}")
        except Exception as e:
            print(f"   ❌ Pending signatures check failed: {e}")
        
        # Summary
        print("\n" + "=" * 40)
        if all_healthy:
            print("🎉 All components are working correctly!")
            print("✅ NDA Agent is ready for use")
            return True
        else:
            print("⚠️  Some components have issues but agent is partially functional")
            return False
            
    except Exception as e:
        logger.error(f"Error during testing: {e}")
        print(f"❌ Critical error during testing: {e}")
        return False


def test_individual_components():
    """Test individual components separately"""
    print("\n🔍 Individual Component Tests")
    print("=" * 40)
    
    try:
        config = Config()
        
        # Test PandaDoc API
        print("1. Testing PandaDoc API...")
        from agents.nda_agent.pandadoc_api import PandaDocAPI
        
        pandadoc = PandaDocAPI(config.pandadoc_api_key)
        templates = pandadoc.list_templates()
        
        if "error" not in templates:
            template_count = len(templates.get("results", []))
            print(f"   ✅ PandaDoc API works - Found {template_count} templates")
        else:
            print(f"   ❌ PandaDoc API error: {templates['error']}")
        
        # Test Google Sheets
        print("\n2. Testing Google Sheets...")
        from agents.nda_agent.google_sheets import GoogleSheetsAPI
        
        sheets = GoogleSheetsAPI(
            config.google_sheets_credentials_path,
            config.google_sheets_spreadsheet_id
        )
        
        if sheets.service:
            print("   ✅ Google Sheets service initialized")
        else:
            print("   ⚠️  Google Sheets not configured or unavailable")
        
        # Test Notifier
        print("\n3. Testing Notifier...")
        from agents.nda_agent.notifier import Notifier
        
        notifier = Notifier(config.get_notification_config())
        
        if notifier.enabled:
            print("   ✅ Email notifications are configured")
        else:
            print("   ⚠️  Email notifications not configured")
        
    except Exception as e:
        print(f"❌ Error testing individual components: {e}")


if __name__ == "__main__":
    print("🚀 NDA Agent Component Testing")
    print("=" * 50)
    
    # Run main test
    success = test_agent_components()
    
    # Run individual component tests
    test_individual_components()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Testing completed successfully!")
        sys.exit(0)
    else:
        print("⚠️  Testing completed with some issues")
        sys.exit(1)
