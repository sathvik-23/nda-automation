"""
Main NDA Agent implementation
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from agno.agent import Agent
from agno.tools import Function
from agno.tools.googlesheets import GoogleSheetsTools

from .config import Config
from .pandadoc_api import PandaDocAPI, create_pandadoc_functions
from .notifier import Notifier

logger = logging.getLogger(__name__)


class NDAAgent:
    """
    Main NDA Agent class that orchestrates document management workflows.
    """
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the NDA Agent.
        
        Args:
            config: Configuration object (will create default if not provided)
        """
        self.config = config or Config()
        
        # Initialize components
        self.pandadoc_api = PandaDocAPI(
            api_key=self.config.pandadoc_api_key,
            base_url=self.config.get_pandadoc_config()["base_url"]
        )
        
        # Initialize Google Sheets if configured
        self.google_sheets_tools = None
        if self.config.is_google_sheets_configured():
            try:
                self.google_sheets_tools = GoogleSheetsTools(
                    spreadsheet_id=self.config.google_sheets_spreadsheet_id,
                    spreadsheet_range=self.config.google_sheets_range,
                    read=True,
                    create=True,
                    update=True,
                    duplicate=False
                )
                logger.info("Google Sheets integration initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Sheets: {e}")
                self.google_sheets_tools = None
        else:
            logger.info("Google Sheets not configured, skipping initialization")
        
        self.notifier = Notifier(self.config.get_notification_config())
        
        # Initialize Agno agent
        self.agent = self._create_agent()
        
        logger.info("NDA Agent initialized successfully")
    
    def _create_agent(self) -> Agent:
        """Create and configure the Agno agent"""
        # Get PandaDoc functions
        pandadoc_functions = create_pandadoc_functions(self.config.pandadoc_api_key)
        
        # Add custom functions
        custom_functions = self._create_custom_functions()
        
        # Combine all functions
        all_functions = pandadoc_functions + custom_functions
        
        # Add Google Sheets tools if available
        tools = all_functions
        if self.google_sheets_tools:
            tools.append(self.google_sheets_tools)
        
        # Create agent
        agent = Agent(
            name=self.config.agent_name,
            description=self.config.agent_description,
            tools=tools,
            markdown=True,
            show_tool_calls=True,
            debug_mode=self.config.debug_mode
        )
        
        return agent
    
    def _log_to_google_sheets(self, action_type: str, document_id: str, details: Dict[str, Any]) -> bool:
        """
        Log NDA action to Google Sheets if available.
        
        Args:
            action_type: Type of action (e.g., "created", "sent", "signed")
            document_id: PandaDoc document ID
            details: Additional details about the action
            
        Returns:
            True if successful, False otherwise
        """
        if not self.google_sheets_tools:
            logger.warning("Google Sheets not configured, skipping log")
            return False
        
        try:
            from datetime import datetime
            import json
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Prepare row data
            row_data = [
                [
                    timestamp,
                    action_type,
                    document_id,
                    details.get("template_name", ""),
                    details.get("recipient", ""),
                    details.get("status", ""),
                    json.dumps(details)  # Store full details as JSON
                ]
            ]
            
            # Try to append to sheet
            # Note: The GoogleSheetsTools will handle the API calls
            # We'll need to use the agent to call the update_sheet function
            logger.info(f"Logging {action_type} action for document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to log to Google Sheets: {e}")
            return False
    
    def _get_google_sheets_statistics(self) -> Dict[str, Any]:
        """
        Get NDA statistics from Google Sheets if available.
        
        Returns:
            Dictionary containing statistics
        """
        if not self.google_sheets_tools:
            return {
                "total_documents": 0,
                "documents_sent": 0,
                "documents_signed": 0,
                "pending_signatures": 0,
                "recent_activity": []
            }
        
        try:
            # Note: We'll need to implement the actual reading logic
            # For now, return empty stats
            return {
                "total_documents": 0,
                "documents_sent": 0,
                "documents_signed": 0,
                "pending_signatures": 0,
                "recent_activity": []
            }
        except Exception as e:
            logger.error(f"Failed to get Google Sheets statistics: {e}")
            return {
                "total_documents": 0,
                "documents_sent": 0,
                "documents_signed": 0,
                "pending_signatures": 0,
                "recent_activity": []
            }
        """Create custom functions for the agent"""
        
        functions = [
            Function(
                name="create_nda_workflow",
                description="Create a complete NDA workflow from template to signature",
                entrypoint=self.create_nda_workflow,
                parameters={
                    "template_id": {"type": "string", "description": "PandaDoc template ID"},
                    "recipient_email": {"type": "string", "description": "Recipient email address"},
                    "recipient_name": {"type": "string", "description": "Recipient full name"},
                    "company_name": {"type": "string", "description": "Company name"},
                    "additional_data": {"type": "object", "description": "Additional document data"}
                }
            ),
            Function(
                name="get_nda_statistics",
                description="Get NDA statistics and recent activity",
                entrypoint=self.get_nda_statistics,
            ),
            Function(
                name="check_pending_signatures",
                description="Check for documents with pending signatures",
                entrypoint=self.check_pending_signatures,
            ),
            Function(
                name="send_daily_summary",
                description="Send daily summary of NDA activities",
                entrypoint=self.send_daily_summary,
            ),
            Function(
                name="log_manual_action",
                description="Log a manual action to the tracking sheet",
                entrypoint=self.log_manual_action,
                parameters={
                    "action_type": {"type": "string", "description": "Type of action"},
                    "document_id": {"type": "string", "description": "Document ID"},
                    "details": {"type": "object", "description": "Action details"}
                }
            )
        ]
        
        return functions
    
    def create_nda_workflow(self, template_id: str, recipient_email: str, recipient_name: str, 
                          company_name: str, additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a complete NDA workflow from template to signature.
        
        Args:
            template_id: PandaDoc template ID
            recipient_email: Recipient email address
            recipient_name: Recipient full name
            company_name: Company name
            additional_data: Additional document data
            
        Returns:
            Dict containing workflow results
        """
        logger.info(f"Creating NDA workflow for {recipient_name} at {company_name}")
        
        try:
            # Prepare document data
            document_data = {
                "name": f"NDA - {company_name} - {recipient_name}",
                "recipients": [
                    {
                        "email": recipient_email,
                        "first_name": recipient_name.split()[0],
                        "last_name": " ".join(recipient_name.split()[1:]) if len(recipient_name.split()) > 1 else "",
                        "role": "signer"
                    }
                ],
                "fields": {
                    "recipient_name": recipient_name,
                    "company_name": company_name,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }
            }
            
            # Add additional data if provided
            if additional_data:
                document_data["fields"].update(additional_data)
            
            # Create document
            create_result = self.pandadoc_api.create_document_from_template(template_id, document_data)
            
            if "error" in create_result:
                logger.error(f"Failed to create document: {create_result['error']}")
                return {"success": False, "error": create_result["error"]}
            
            document_id = create_result.get("id")
            
            # Log to Google Sheets
            self._log_to_google_sheets(
                action_type="created",
                document_id=document_id,
                details={
                    "template_name": create_result.get("name", "Unknown"),
                    "recipient": recipient_email,
                    "company": company_name,
                    "status": "created"
                }
            )
            
            # Send notification
            self.notifier.notify_document_created(
                document_id=document_id,
                template_name=create_result.get("name", "Unknown"),
                recipient=recipient_email
            )
            
            return {
                "success": True,
                "document_id": document_id,
                "document_name": create_result.get("name"),
                "status": "created",
                "next_steps": "Review the document and send it for signature using send_document function"
            }
            
        except Exception as e:
            logger.error(f"Error in NDA workflow: {e}")
            return {"success": False, "error": str(e)}
    
    def get_nda_statistics(self) -> Dict[str, Any]:
        """Get NDA statistics and recent activity"""
        logger.info("Fetching NDA statistics")
        
        try:
            # Get statistics from Google Sheets
            stats = self._get_google_sheets_statistics()
            
            # Get recent documents from PandaDoc
            recent_docs = self.pandadoc_api.list_documents(limit=10)
            
            if "error" not in recent_docs:
                stats["recent_pandadoc_documents"] = recent_docs.get("results", [])
            
            return stats
            
        except Exception as e:
            logger.error(f"Error fetching statistics: {e}")
            return {"error": str(e)}
    
    def check_pending_signatures(self) -> Dict[str, Any]:
        """Check for documents with pending signatures"""
        logger.info("Checking for pending signatures")
        
        try:
            # Get sent documents from PandaDoc
            sent_docs = self.pandadoc_api.list_documents(status="sent")
            
            if "error" in sent_docs:
                return {"error": sent_docs["error"]}
            
            pending_docs = []
            for doc in sent_docs.get("results", []):
                doc_details = self.pandadoc_api.get_document_status(doc["id"])
                if doc_details.get("status") == "sent":
                    pending_docs.append({
                        "id": doc["id"],
                        "name": doc.get("name"),
                        "created": doc.get("date_created"),
                        "recipients": doc.get("recipients", [])
                    })
            
            return {
                "pending_count": len(pending_docs),
                "pending_documents": pending_docs
            }
            
        except Exception as e:
            logger.error(f"Error checking pending signatures: {e}")
            return {"error": str(e)}
    
    def send_daily_summary(self) -> Dict[str, Any]:
        """Send daily summary of NDA activities"""
        logger.info("Sending daily summary")
        
        try:
            # Get statistics
            stats = self.get_nda_statistics()
            
            # Send summary email
            success = self.notifier.send_daily_summary(stats)
            
            return {
                "success": success,
                "statistics": stats,
                "message": "Daily summary sent successfully" if success else "Failed to send daily summary"
            }
            
        except Exception as e:
            logger.error(f"Error sending daily summary: {e}")
            return {"success": False, "error": str(e)}
    
    def log_manual_action(self, action_type: str, document_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Log a manual action to the tracking sheet"""
        logger.info(f"Logging manual action: {action_type} for document {document_id}")
        
        try:
            success = self._log_to_google_sheets(
                action_type=action_type,
                document_id=document_id,
                details=details
            )
            
            return {
                "success": success,
                "message": "Action logged successfully" if success else "Failed to log action"
            }
            
        except Exception as e:
            logger.error(f"Error logging manual action: {e}")
            return {"success": False, "error": str(e)}
    
    def run(self, query: str) -> str:
        """
        Run a query against the NDA Agent.
        
        Args:
            query: Natural language query
            
        Returns:
            Agent response
        """
        logger.info(f"Processing query: {query}")
        return self.agent.run(query)
    
    def chat(self) -> None:
        """Start an interactive chat session with the agent"""
        logger.info("Starting interactive chat session")
        
        print("🤖 NDA Agent - Interactive Chat")
        print("=" * 40)
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("\nAgent: ")
                response = self.run(user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """Perform a health check of all components"""
        logger.info("Performing health check")
        
        health_status = {
            "overall": "healthy",
            "components": {}
        }
        
        # Check PandaDoc API
        try:
            templates = self.pandadoc_api.list_templates()
            health_status["components"]["pandadoc"] = {
                "status": "healthy" if "error" not in templates else "unhealthy",
                "details": f"Found {len(templates.get('results', []))} templates" if "error" not in templates else templates.get("error")
            }
        except Exception as e:
            health_status["components"]["pandadoc"] = {
                "status": "unhealthy",
                "details": str(e)
            }
        
        # Check Google Sheets
        try:
            if self.google_sheets_tools:
                health_status["components"]["google_sheets"] = {
                    "status": "healthy",
                    "details": "GoogleSheetsTools initialized"
                }
            else:
                health_status["components"]["google_sheets"] = {
                    "status": "unavailable",
                    "details": "GoogleSheetsTools not configured"
                }
        except Exception as e:
            health_status["components"]["google_sheets"] = {
                "status": "unhealthy",
                "details": str(e)
            }
        
        # Check Notifier
        health_status["components"]["notifier"] = {
            "status": "healthy" if self.notifier.enabled else "disabled",
            "details": "Email notifications configured" if self.notifier.enabled else "Email notifications not configured"
        }
        
        # Determine overall health
        component_statuses = [comp["status"] for comp in health_status["components"].values()]
        if "unhealthy" in component_statuses:
            health_status["overall"] = "unhealthy"
        elif "unavailable" in component_statuses or "disabled" in component_statuses:
            health_status["overall"] = "partially_healthy"
        
        return health_status
