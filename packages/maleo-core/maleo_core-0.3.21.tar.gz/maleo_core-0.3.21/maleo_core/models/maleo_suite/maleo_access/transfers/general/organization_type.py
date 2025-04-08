from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoAccessOrganizationTypeGeneralTransfers:
    class Base(BaseModel):
        order:Optional[int] = Field(None, ge=1, description="Organization Type's order")
        key:str = Field(..., max_length=20, description="Organization Type's key")
        name:str = Field(..., max_length=20, description="Organization Type's name")