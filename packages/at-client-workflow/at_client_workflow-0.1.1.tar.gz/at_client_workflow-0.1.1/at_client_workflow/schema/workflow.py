from at_common_schemas.base import BaseSchema
from typing import Optional, Dict, Any
from pydantic import Field

class ExecuteRequest(BaseSchema):
    """Request to execute a workflow with optional input."""
    name: str = Field(..., description="The name of the workflow to execute.")
    initial_context: Optional[Dict[str, Any]] = Field(None, description="Optional input for the workflow execution.")

class ExecuteResponse(BaseSchema):
    """Response from a workflow execution."""
    result: Dict[str, Any] = Field(..., description="The result of the workflow execution.")

class WorkflowEvent(BaseSchema):
    """A single event from a workflow execution."""
    type: str = Field(..., description="The type of workflow event.")
    content: Optional[str] = Field(None, description="The content of the event, if applicable.")
    task_name: Optional[str] = Field(None, description="The name of the task, if applicable.")
    result: Optional[Dict[str, Any]] = Field(None, description="The result of the task, if applicable.")
    workflow_name: Optional[str] = Field(None, description="The name of the workflow, if applicable.")
    error: Optional[str] = Field(None, description="Error message, if an error occurred.")