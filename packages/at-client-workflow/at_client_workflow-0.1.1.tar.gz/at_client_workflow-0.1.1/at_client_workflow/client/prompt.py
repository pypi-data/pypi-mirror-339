"""
Core API client for the AT Backend Workflow Prompt service.
"""
import logging
from typing import List, Optional

from .base import BaseClient
from app.schema.prompt import (
    ListResponse,
    CountResponse,
    CreateResponse,
    UpdateResponse,
    DeleteResponse
)

logger = logging.getLogger(__name__)

class PromptClient(BaseClient):
    """Client for the AT Backend Workflow Prompt API."""
    
    def __init__(self, host: str, port: int):
        """
        Initialize the Core API client.
        
        Args:
            host: Host name
            port: Port number
        """
        super().__init__(host, port)
        self.base_url = f"{self.base_url}/prompt"
    
    async def list_prompts(self) -> ListResponse:
        """
        List all available prompts.
        
        Returns:
            List of Prompt objects
        """
        response = await self.get("list")
        return ListResponse(**response)
    
    async def count_prompts(self) -> CountResponse:
        """
        Count all available prompts.
        
        Returns:
            Number of prompts
        """
        response = await self.get("count")
        return CountResponse(**response)
    
    async def create_prompt(
        self,
        name: str,
        description: str,
        tags: List[str],
        model: str,
        sys_tpl: str,
        usr_tpl: str
    ) -> CreateResponse:
        """
        Create a new prompt.
        
        Args:
            name: Name of the prompt
            description: Description of the prompt
            tags: List of tags
            model: Model to use
            sys_tpl: System template
            usr_tpl: User template
            
        Returns:
            Created Prompt object
        """
        request_data = {
            "name": name,
            "description": description,
            "tags": tags,
            "model": model,
            "sys_tpl": sys_tpl,
            "usr_tpl": usr_tpl
        }
        response = await self.post("create", json=request_data)
        return CreateResponse(**response)
    
    async def update_prompt(
        self,
        name: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        model: Optional[str] = None,
        sys_tpl: Optional[str] = None,
        usr_tpl: Optional[str] = None
    ) -> UpdateResponse:
        """
        Update an existing prompt.
        
        Args:
            name: Name of the prompt to update
            description: Optional new description
            tags: Optional new tags
            model: Optional new model
            sys_tpl: Optional new system template
            usr_tpl: Optional new user template
            
        Returns:
            Updated Prompt object
        """
        request_data = {"name": name}
        
        # Only include fields that are provided
        if description is not None:
            request_data["description"] = description
        if tags is not None:
            request_data["tags"] = tags
        if model is not None:
            request_data["model"] = model
        if sys_tpl is not None:
            request_data["sys_tpl"] = sys_tpl
        if usr_tpl is not None:
            request_data["usr_tpl"] = usr_tpl
        
        # Use PUT method since the endpoint is a PUT
        response = await self.put("update", json=request_data)
        return UpdateResponse(**response)
    
    async def delete_prompt(self, name: str) -> DeleteResponse:
        """
        Delete a prompt.
        
        Args:
            name: Name of the prompt to delete
            
        Returns:
            DeleteResponse object
        """
        params = {"name": name}
        response = await self.delete("delete", params=params)
        return DeleteResponse(**response)

    