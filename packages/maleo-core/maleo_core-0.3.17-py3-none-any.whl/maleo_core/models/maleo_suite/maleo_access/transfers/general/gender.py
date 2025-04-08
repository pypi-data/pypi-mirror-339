from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoAccessGenderGeneralTransfers:
    class Base(BaseModel):
        order:Optional[int] = Field(None, ge=1, description="Gender's order")
        key:str = Field(..., max_length=15, description="Gender's key")
        name:str = Field(..., max_length=15, description="Gender's name")