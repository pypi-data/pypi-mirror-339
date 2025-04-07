from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoAccessSystemRoleGeneralTransfers:
    class Base(BaseModel):
        order:Optional[int] = Field(None, ge=1, description="System Role's order")
        key:str = Field(..., max_length=20, description="System Role's key")
        name:str = Field(..., max_length=20, description="System Role's name")
        description:str = Field(..., max_length=50, description="System Role's description")
        icon:str = Field("Circle", max_length=20, description="System Role's icon")