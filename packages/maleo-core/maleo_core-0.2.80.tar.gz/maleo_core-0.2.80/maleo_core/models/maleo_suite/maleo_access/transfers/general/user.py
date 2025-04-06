from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional

class MaleoAccessUserGeneralTransfers:
    class Base(BaseModel):
        username:Optional[str] = Field(..., max_length=50, description="User's username")
        email:str = Field(..., max_length=255, description="User's email")
        phone:str = Field(..., max_length=15, description="User's phone")
        user_type_id:int = Field(..., ge=1, description="User's type id")