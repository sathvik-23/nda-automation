"""
Enhanced PandaDoc API integration module for Phase 2
"""

import requests
from typing import Dict, Any, List, Optional
from agno.tools import Function
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class PandaDocAPI:
    """Enhanced PandaDoc API client for document management"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.pandadoc.com/public/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"API-Key {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to PandaDoc API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"PandaDoc API request failed: {e}")
            return {"error": str(e)}
    
    def list_templates(self) -> Dict[str, Any]:
        """
        List all available templates from PandaDoc account.
        
        Returns:
            Dict containing template information
        """
        logger.info("Fetching templates from PandaDoc")
        return self._make_request("GET", "/templates")
    
    def get_template_details(self, template_id: str) -> Dict[str, Any]:
        """
        Get details for a specific template.
        
        Args:
            template_id: The ID of the template to retrieve
            
        Returns:
            Dict containing template details
        """
        logger.info(f"Fetching template details for ID: {template_id}")
        return self._make_request("GET", f"/templates/{template_id}/details")
    
    def create_document(self, name: str, template_id: str, recipient: Dict[str, Any], tokens: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Create document from template (Phase 2 enhanced version).
        
        Args:
            name: Document name
            template_id: Template UUID
            recipient: Recipient information dict
            tokens: List of token name-value pairs
            
        Returns:
            Dict containing created document information
        """
        logger.info(f"Creating document '{name}' from template: {template_id}")
        
        data = {
            "name": name,
            "template_uuid": template_id,
            "recipients": [recipient],
            "tokens": tokens
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/documents",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"Document created successfully with ID: {result.get('id')}")
            return result
        except requests.RequestException as e:
            logger.error(f"Failed to create document: {e}")
            return {"error": str(e)}
    
    def create_document_from_template(self, template_id: str, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a document from a template (legacy method).
        
        Args:
            template_id: The ID of the template to use
            document_data: Data to populate the document
            
        Returns:
            Dict containing the created document information
        """
        logger.info(f"Creating document from template: {template_id}")
        
        payload = {
            "template_uuid": template_id,
            **document_data
        }
        
        return self._make_request("POST", "/documents", data=payload)
    
    def send_document(self, document_id: str, message: str = "") -> Dict[str, Any]:
        """
        Send document for signature (Phase 2 enhanced version).
        
        Args:
            document_id: Document ID to send
            message: Optional message to include
            
        Returns:
            Dict containing send status
        """
        logger.info(f"Sending document for signature: {document_id}")
        
        data = {
            "message": message,
            "silent": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/documents/{document_id}/send",
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            logger.info(f"Document {document_id} sent successfully")
            return {"status": "sent", "document_id": document_id}
        except requests.RequestException as e:
            logger.error(f"Failed to send document: {e}")
            return {"error": str(e)}
    
    def get_document_details(self, document_id: str) -> Dict[str, Any]:
        """
        Get details for a specific document.
        
        Args:
            document_id: The ID of the document to retrieve
            
        Returns:
            Dict containing document details
        """
        logger.info(f"Fetching document details for ID: {document_id}")
        return self._make_request("GET", f"/documents/{document_id}/details")
    
    def get_document_status(self, document_id: str) -> Dict[str, Any]:
        """
        Get the current status of a document.
        
        Args:
            document_id: The ID of the document
            
        Returns:
            Dict containing document status
        """
        logger.info(f"Checking document status for ID: {document_id}")
        return self._make_request("GET", f"/documents/{document_id}")
    
    def download_document(self, document_id: str, save_path: str = None) -> Dict[str, Any]:
        """
        Download a completed document.
        
        Args:
            document_id: The ID of the document to download
            save_path: Optional path to save the document
            
        Returns:
            Dict containing download result
        """
        logger.info(f"Downloading document: {document_id}")
        
        try:
            # Get document download URL
            url = f"{self.base_url}/documents/{document_id}/download"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Save the document
            if save_path is None:
                save_path = f"document_{document_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Document downloaded successfully to: {save_path}")
            return {
                "status": "downloaded",
                "file_path": save_path,
                "file_size": len(response.content)
            }
        except requests.RequestException as e:
            logger.error(f"Failed to download document: {e}")
            return {"error": str(e)}
    
    def list_documents(self, status: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """
        List documents with optional filtering.
        
        Args:
            status: Optional status filter (draft, sent, completed, etc.)
            limit: Number of documents to return
            
        Returns:
            Dict containing list of documents
        """
        logger.info(f"Listing documents with status: {status}")
        
        # Build endpoint with query parameters
        endpoint = "/documents"
        params = []
        
        if limit:
            params.append(f"count={limit}")
        
        if status:
            params.append(f"status={status}")
        
        if params:
            endpoint += "?" + "&".join(params)
        
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"PandaDoc API request failed: {e}")
            # Return empty result instead of error to avoid breaking the workflow
            return {"results": [], "count": 0}
    
    def create_and_send_nda(self, name: str, template_id: str, recipient: Dict[str, Any], tokens: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Complete workflow: Create document and send for signature.
        
        Args:
            name: Document name
            template_id: Template UUID
            recipient: Recipient information
            tokens: Document tokens/variables
            
        Returns:
            Dict containing complete workflow result
        """
        logger.info(f"Starting complete NDA workflow for: {name}")
        
        # Step 1: Create document
        doc_result = self.create_document(name, template_id, recipient, tokens)
        
        if "error" in doc_result:
            return {"error": "Document creation failed", "details": doc_result}
        
        if "id" not in doc_result:
            return {"error": "Document creation failed - no ID returned", "details": doc_result}
        
        document_id = doc_result["id"]
        
        # Step 2: Send for signature
        send_result = self.send_document(document_id)
        
        if "error" in send_result:
            return {
                "error": "Document created but sending failed",
                "document": doc_result,
                "send_error": send_result
            }
        
        # Step 3: Return complete result
        return {
            "success": True,
            "document": doc_result,
            "send_status": send_result,
            "document_id": document_id,
            "workflow_completed": True
        }


def create_pandadoc_functions(api_key: str) -> List[Function]:
    """
    Create agno Function objects for PandaDoc API operations.
    
    Args:
        api_key: PandaDoc API key
        
    Returns:
        List of Function objects for use with agno Agent
    """
    pandadoc_api = PandaDocAPI(api_key)
    
    functions = [
        Function(
            name="list_templates",
            description="List all available templates from PandaDoc account",
            entrypoint=pandadoc_api.list_templates,
        ),
        Function(
            name="get_template_details",
            description="Get details for a specific template",
            entrypoint=pandadoc_api.get_template_details,
            parameters={
                "template_id": {"type": "string", "description": "The ID of the template to retrieve"}
            }
        ),
        Function(
            name="create_document",
            description="Create a document from template with recipient and tokens",
            entrypoint=pandadoc_api.create_document,
            parameters={
                "name": {"type": "string", "description": "Document name"},
                "template_id": {"type": "string", "description": "Template UUID"},
                "recipient": {"type": "object", "description": "Recipient information"},
                "tokens": {"type": "array", "description": "Document tokens/variables"}
            }
        ),
        Function(
            name="create_document_from_template",
            description="Create a document from a template (legacy method)",
            entrypoint=pandadoc_api.create_document_from_template,
            parameters={
                "template_id": {"type": "string", "description": "The ID of the template to use"},
                "document_data": {"type": "object", "description": "Data to populate the document"}
            }
        ),
        Function(
            name="send_document",
            description="Send a document for signature",
            entrypoint=pandadoc_api.send_document,
            parameters={
                "document_id": {"type": "string", "description": "The ID of the document to send"},
                "message": {"type": "string", "description": "Optional message to include"}
            }
        ),
        Function(
            name="get_document_status",
            description="Get the current status of a document",
            entrypoint=pandadoc_api.get_document_status,
            parameters={
                "document_id": {"type": "string", "description": "The ID of the document"}
            }
        ),
        Function(
            name="download_document",
            description="Download a completed document",
            entrypoint=pandadoc_api.download_document,
            parameters={
                "document_id": {"type": "string", "description": "The ID of the document to download"},
                "save_path": {"type": "string", "description": "Optional path to save the document"}
            }
        ),
        Function(
            name="create_and_send_nda",
            description="Complete workflow: Create document and send for signature",
            entrypoint=pandadoc_api.create_and_send_nda,
            parameters={
                "name": {"type": "string", "description": "Document name"},
                "template_id": {"type": "string", "description": "Template UUID"},
                "recipient": {"type": "object", "description": "Recipient information"},
                "tokens": {"type": "array", "description": "Document tokens/variables"}
            }
        ),
        Function(
            name="list_documents",
            description="List documents with optional filtering",
            entrypoint=pandadoc_api.list_documents,
            parameters={
                "status": {"type": "string", "description": "Optional status filter (draft, sent, completed, etc.)"},
                "limit": {"type": "integer", "description": "Number of documents to return (default: 100)"}
            }
        )
    ]
    
    return functions


# For direct testing when run as script
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Initialize API
    api_key = os.getenv("PANDADOC_API_KEY")
    if not api_key:
        print("❌ PANDADOC_API_KEY not found in environment variables")
        exit(1)
    
    pandadoc = PandaDocAPI(api_key)
    
    # Test 1: List templates
    print("🔍 Testing template listing...")
    templates = pandadoc.list_templates()
    
    if "error" in templates:
        print(f"❌ Error: {templates['error']}")
    else:
        print(f"✅ Found {len(templates.get('results', []))} templates")
        for template in templates.get('results', []):
            print(f"  • {template.get('name')} (ID: {template.get('id')})")
    
    print("\n🎯 PandaDoc API Phase 2 Enhancement Complete!")
    print("Ready for create_document and send_document operations.")
