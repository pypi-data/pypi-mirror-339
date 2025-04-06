from __future__ import annotations
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

class MaleoAccessUserProfileGeneralTransfers:
    class Base(BaseModel):
        user_id:int = Field(..., ge=1, description="User's id")
        id_card:Optional[str] = Field(None, max_length=16, description="User's id card")
        leading_title:Optional[str] = Field(None, max_length=25, description="User's leading title")
        first_name:str = Field(..., max_length=50, description="User's first name")
        middle_name:Optional[str] = Field(None, max_length=50, description="User's middle name")
        last_name:str = Field(..., max_length=50, description="User's last name")
        ending_title:Optional[str] = Field(None, max_length=25, description="User's ending title")
        full_name:Optional[str] = Field(None, max_length=200, description="User's full name")
        birth_place:Optional[str] = Field(None, max_length=50, description="User's birth place")
        birth_date:Optional[date] = Field(None, description="User's birth date")
        gender_id:Optional[int] = Field(None, ge=1, description="User's gender's id")
        blood_type_id:Optional[int] = Field(None, ge=1, description="User's blood type's id")