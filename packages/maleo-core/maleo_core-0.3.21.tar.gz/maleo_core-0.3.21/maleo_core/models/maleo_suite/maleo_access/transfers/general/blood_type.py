from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoAccessBloodTypeGeneralTransfers:
    class Base(BaseModel):
        order:Optional[int] = Field(None, ge=1, description="Blood Type's order")
        key:str = Field(..., max_length=2, description="Blood Type's key")
        name:str = Field(..., max_length=2, description="Blood Type's name")