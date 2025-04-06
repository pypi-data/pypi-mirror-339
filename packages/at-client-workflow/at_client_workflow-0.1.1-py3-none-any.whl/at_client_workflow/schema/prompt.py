from typing import List, Optional
from pydantic import Field
from at_common_schemas.base import BaseSchema

class Prompt(BaseSchema):
    name: str = Field(..., description="The name of the prompt")
    description: str = Field(..., description="The description of the prompt")
    tags: List[str] = Field(..., description="The tags of the prompt")
    model: str = Field(..., description="The model to use for the prompt")
    sys_tpl: str = Field(..., description="The system template of the prompt")
    usr_tpl: str = Field(..., description="The user template of the prompt")

class ListRequest(BaseSchema):
    pass

class ListResponse(BaseSchema):
    prompts: List[Prompt] = Field(..., description="The list of prompts")

class CountRequest(BaseSchema):
    pass

class CountResponse(BaseSchema):
    num: int = Field(..., description="The number of prompts")

class CreateRequest(Prompt):
    pass
    
class CreateResponse(Prompt):
    pass

class UpdateRequest(Prompt):
    description: Optional[str] = Field(None, description="The description of the prompt")
    tags: Optional[List[str]] = Field(None, description="The tags of the prompt")
    model: Optional[str] = Field(None, description="The model to use for the prompt")
    sys_tpl: Optional[str] = Field(None, description="The system template of the prompt")
    usr_tpl: Optional[str] = Field(None, description="The user template of the prompt")

class UpdateResponse(Prompt):
    pass

class DeleteRequest(BaseSchema):
    name: str = Field(..., description="The name of the prompt")

class DeleteResponse(BaseSchema):
    pass