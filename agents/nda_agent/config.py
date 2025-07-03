"""
Configuration module for NDA Agent
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for NDA Agent"""
    
    def __init__(self):
        self.pandadoc_api_key = os.getenv("PANDADOC_API_KEY")
        
        # Google Sheets OAuth Configuration
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.google_project_id = os.getenv("GOOGLE_PROJECT_ID")
        self.google_redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8080")
        self.google_sheets_spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        self.google_sheets_range = os.getenv("GOOGLE_SHEETS_RANGE", "NDA_Log!A:G")
        
        # Email notifications
        self.notification_email = os.getenv("NOTIFICATION_EMAIL")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        
        # Agent settings
        self.agent_name = os.getenv("AGENT_NAME", "NDA Agent")
        self.agent_description = os.getenv("AGENT_DESCRIPTION", "AI agent for NDA document management")
        self.debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"
        self.verbose_logging = os.getenv("VERBOSE_LOGGING", "False").lower() == "true"
        
        # Validate required configurations
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate required configuration values"""
        required_configs = {
            "PANDADOC_API_KEY": self.pandadoc_api_key,
        }
        
        missing_configs = [key for key, value in required_configs.items() if not value]
        
        if missing_configs:
            raise ValueError(f"Missing required configuration: {', '.join(missing_configs)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "pandadoc_api_key": "***" if self.pandadoc_api_key else None,
            "google_client_id": "***" if self.google_client_id else None,
            "google_client_secret": "***" if self.google_client_secret else None,
            "google_project_id": self.google_project_id,
            "google_redirect_uri": self.google_redirect_uri,
            "google_sheets_spreadsheet_id": self.google_sheets_spreadsheet_id,
            "google_sheets_range": self.google_sheets_range,
            "notification_email": self.notification_email,
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port,
            "smtp_username": self.smtp_username,
            "agent_name": self.agent_name,
            "agent_description": self.agent_description,
            "debug_mode": self.debug_mode,
            "verbose_logging": self.verbose_logging,
        }
    
    def get_pandadoc_config(self) -> Dict[str, Any]:
        """Get PandaDoc specific configuration"""
        return {
            "api_key": self.pandadoc_api_key,
            "base_url": "https://api.pandadoc.com/public/v1"
        }
    
    def get_google_sheets_config(self) -> Dict[str, Any]:
        """Get Google Sheets specific configuration"""
        return {
            "client_id": self.google_client_id,
            "client_secret": self.google_client_secret,
            "project_id": self.google_project_id,
            "redirect_uri": self.google_redirect_uri,
            "spreadsheet_id": self.google_sheets_spreadsheet_id,
            "spreadsheet_range": self.google_sheets_range
        }
    
    def get_notification_config(self) -> Dict[str, Any]:
        """Get notification specific configuration"""
        return {
            "email": self.notification_email,
            "smtp_server": self.smtp_server,
            "smtp_port": self.smtp_port,
            "smtp_username": self.smtp_username,
            "smtp_password": self.smtp_password
        }
    
    def is_google_sheets_configured(self) -> bool:
        """Check if Google Sheets is properly configured"""
        return all([
            self.google_client_id,
            self.google_client_secret,
            self.google_project_id,
            self.google_sheets_spreadsheet_id
        ])
