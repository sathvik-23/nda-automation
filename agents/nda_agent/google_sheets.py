"""
Google Sheets API integration module
"""

import os
import json
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_SHEETS_AVAILABLE = True
except ImportError:
    GOOGLE_SHEETS_AVAILABLE = False
    logger.warning("Google Sheets API libraries not installed. Install with: pip install google-api-python-client google-auth")


class GoogleSheetsAPI:
    """Google Sheets API client for spreadsheet management"""
    
    def __init__(self, credentials_path: Optional[str] = None, spreadsheet_id: Optional[str] = None):
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.service = None
        
        if not GOOGLE_SHEETS_AVAILABLE:
            logger.error("Google Sheets API libraries not available")
            return
        
        if credentials_path and os.path.exists(credentials_path):
            self._initialize_service()
        else:
            logger.warning("Google Sheets credentials not found or not provided")
    
    def _initialize_service(self) -> None:
        """Initialize Google Sheets service"""
        try:
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            credentials = Credentials.from_service_account_file(
                self.credentials_path, scopes=scopes
            )
            self.service = build('sheets', 'v4', credentials=credentials)
            logger.info("Google Sheets service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {e}")
    
    def read_sheet(self, sheet_name: str, range_name: str = "A:Z") -> List[List[str]]:
        """
        Read data from a Google Sheet.
        
        Args:
            sheet_name: Name of the sheet tab
            range_name: Cell range to read (e.g., "A1:D10")
            
        Returns:
            List of rows, where each row is a list of cell values
        """
        if not self.service:
            logger.error("Google Sheets service not initialized")
            return []
        
        try:
            range_spec = f"{sheet_name}!{range_name}"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_spec
            ).execute()
            
            values = result.get('values', [])
            logger.info(f"Read {len(values)} rows from {range_spec}")
            return values
        except HttpError as e:
            logger.error(f"Failed to read from Google Sheets: {e}")
            return []
    
    def write_sheet(self, sheet_name: str, range_name: str, values: List[List[str]]) -> bool:
        """
        Write data to a Google Sheet.
        
        Args:
            sheet_name: Name of the sheet tab
            range_name: Cell range to write to (e.g., "A1:D10")
            values: List of rows to write
            
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            logger.error("Google Sheets service not initialized")
            return False
        
        try:
            range_spec = f"{sheet_name}!{range_name}"
            body = {
                'values': values
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_spec,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Updated {result.get('updatedCells')} cells in {range_spec}")
            return True
        except HttpError as e:
            logger.error(f"Failed to write to Google Sheets: {e}")
            return False
    
    def append_row(self, sheet_name: str, values: List[str]) -> bool:
        """
        Append a row to a Google Sheet.
        
        Args:
            sheet_name: Name of the sheet tab
            values: List of cell values to append
            
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            logger.error("Google Sheets service not initialized")
            return False
        
        try:
            range_spec = f"{sheet_name}!A:Z"
            body = {
                'values': [values]
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_spec,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Appended row to {sheet_name}")
            return True
        except HttpError as e:
            logger.error(f"Failed to append row to Google Sheets: {e}")
            return False
    
    def create_sheet(self, sheet_name: str) -> bool:
        """
        Create a new sheet tab.
        
        Args:
            sheet_name: Name of the new sheet tab
            
        Returns:
            True if successful, False otherwise
        """
        if not self.service:
            logger.error("Google Sheets service not initialized")
            return False
        
        try:
            body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': sheet_name
                        }
                    }
                }]
            }
            
            result = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
            
            logger.info(f"Created new sheet: {sheet_name}")
            return True
        except HttpError as e:
            logger.error(f"Failed to create sheet: {e}")
            return False
    
    def log_nda_action(self, action_type: str, document_id: str, details: Dict[str, Any]) -> bool:
        """
        Log NDA-related actions to a Google Sheet.
        
        Args:
            action_type: Type of action (e.g., "created", "sent", "signed")
            document_id: PandaDoc document ID
            details: Additional details about the action
            
        Returns:
            True if successful, False otherwise
        """
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare row data
        row_data = [
            timestamp,
            action_type,
            document_id,
            details.get("template_name", ""),
            details.get("recipient", ""),
            details.get("status", ""),
            json.dumps(details)  # Store full details as JSON
        ]
        
        # Try to append to "NDA_Log" sheet
        success = self.append_row("NDA_Log", row_data)
        
        if not success:
            # If sheet doesn't exist, create it with headers
            if self.create_sheet("NDA_Log"):
                headers = [
                    "Timestamp",
                    "Action",
                    "Document ID",
                    "Template Name",
                    "Recipient",
                    "Status",
                    "Details"
                ]
                self.append_row("NDA_Log", headers)
                success = self.append_row("NDA_Log", row_data)
        
        return success
    
    def get_nda_statistics(self) -> Dict[str, Any]:
        """
        Get NDA statistics from the log sheet.
        
        Returns:
            Dictionary containing statistics
        """
        data = self.read_sheet("NDA_Log")
        
        if not data or len(data) < 2:  # No data or only headers
            return {
                "total_documents": 0,
                "documents_sent": 0,
                "documents_signed": 0,
                "pending_signatures": 0,
                "recent_activity": []
            }
        
        # Skip header row
        rows = data[1:]
        
        stats = {
            "total_documents": len(rows),
            "documents_sent": 0,
            "documents_signed": 0,
            "pending_signatures": 0,
            "recent_activity": []
        }
        
        for row in rows:
            if len(row) >= 6:
                action = row[1]
                status = row[5] if len(row) > 5 else ""
                
                if action == "sent":
                    stats["documents_sent"] += 1
                elif action == "signed" or status == "completed":
                    stats["documents_signed"] += 1
                elif status == "sent":
                    stats["pending_signatures"] += 1
                
                # Add to recent activity (last 5 items)
                if len(stats["recent_activity"]) < 5:
                    stats["recent_activity"].append({
                        "timestamp": row[0],
                        "action": action,
                        "document_id": row[2],
                        "template_name": row[3] if len(row) > 3 else "",
                        "recipient": row[4] if len(row) > 4 else ""
                    })
        
        return stats
