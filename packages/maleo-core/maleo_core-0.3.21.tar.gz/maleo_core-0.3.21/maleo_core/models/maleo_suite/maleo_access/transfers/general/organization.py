from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoAccessOrganizationGeneralTransfers:
    class Base(BaseModel):
        organization_type_id:int = Field(1, ge=1, description="Organization's type id")
        parent_organization_id:Optional[int] = Field(None, ge=1, description="Parent organization's id")
        key:str = Field(..., max_length=255, description="Organization's key")
        name:str = Field(..., max_length=255, description="Organization's name")