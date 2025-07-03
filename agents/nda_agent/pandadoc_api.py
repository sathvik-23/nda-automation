"""
PandaDoc API integration module
"""

import requests
from typing import Dict, Any, List, Optional
from agno.tools import Function
import logging

logger = logging.getLogger(__name__)


class PandaDocAPI:
    """PandaDoc API client for document management"""
    
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
    
    def create_document_from_template(self, template_id: str, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a document from a template.
        
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
    
    def send_document(self, document_id: str, message: str = "") -> Dict[str, Any]:
        """
        Send a document for signature.
        
        Args:
            document_id: The ID of the document to send
            message: Optional message to include
            
        Returns:
            Dict containing send result
        """
        logger.info(f"Sending document for signature: {document_id}")
        
        payload = {
            "message": message,
            "silent": False
        }
        
        return self._make_request("POST", f"/documents/{document_id}/send", data=payload)
    
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
            name="create_document_from_template",
            description="Create a document from a template",
            entrypoint=pandadoc_api.create_document_from_template,
            parameters={
                "template_id": {"type": "string", "description": "The ID of the template to use"},
                "document_data": {"type": "object", "description": "Data to populate the document"}
            }
        ),
        Function(
            name="get_document_details",
            description="Get details for a specific document",
            entrypoint=pandadoc_api.get_document_details,
            parameters={
                "document_id": {"type": "string", "description": "The ID of the document to retrieve"}
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
