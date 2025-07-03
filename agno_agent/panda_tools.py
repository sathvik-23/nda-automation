import requests
from agno.tools import Function
from typing import Dict, Any


class PandaDocTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pandadoc.com/public/v1"

    def list_templates(self) -> Dict[str, Any]:
        """
        List all available templates from PandaDoc account.
        
        Returns:
            Dict containing template information
        """
        url = f"{self.base_url}/templates"
        headers = {
            "Authorization": f"API-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching templates: {e}")
            return {"results": [], "error": str(e)}

    def get_template_details(self, template_id: str) -> Dict[str, Any]:
        """
        Get details for a specific template.
        
        Args:
            template_id: The ID of the template to retrieve
            
        Returns:
            Dict containing template details
        """
        url = f"{self.base_url}/templates/{template_id}/details"
        headers = {
            "Authorization": f"API-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching template details: {e}")
            return {"error": str(e)}

    def create_document_from_template(self, template_id: str, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a document from a template.
        
        Args:
            template_id: The ID of the template to use
            document_data: Data to populate the document
            
        Returns:
            Dict containing the created document information
        """
        url = f"{self.base_url}/documents"
        headers = {
            "Authorization": f"API-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "template_uuid": template_id,
            **document_data
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating document: {e}")
            return {"error": str(e)}


def create_pandadoc_functions(api_key: str) -> list:
    """
    Create agno Function objects for PandaDoc API operations.
    
    Args:
        api_key: PandaDoc API key
        
    Returns:
        List of Function objects for use with agno Agent
    """
    panda_tool = PandaDocTool(api_key)
    
    # Create Function objects for agno
    functions = [
        Function(
            name="list_templates",
            description="List all available templates from PandaDoc account",
            entrypoint=panda_tool.list_templates,
        ),
        Function(
            name="get_template_details",
            description="Get details for a specific template",
            entrypoint=panda_tool.get_template_details,
            parameters={
                "template_id": {"type": "string", "description": "The ID of the template to retrieve"}
            }
        ),
        Function(
            name="create_document_from_template",
            description="Create a document from a template",
            entrypoint=panda_tool.create_document_from_template,
            parameters={
                "template_id": {"type": "string", "description": "The ID of the template to use"},
                "document_data": {"type": "object", "description": "Data to populate the document"}
            }
        )
    ]
    
    return functions
