from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional, Union
from uuid import UUID
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters

class MaleoAccessUserGeneralParameters:
    class ExpandableFields(StrEnum):
        TYPE = "user_type"
        PROFILE = "profile"
        GENDER = "profile.gender"
        BLOOD_TYPE = "profile.blood_type"

    expandable_fields:set[ExpandableFields] = {
        ExpandableFields.TYPE,
        ExpandableFields.PROFILE,
        ExpandableFields.GENDER,
        ExpandableFields.BLOOD_TYPE
    }

    class Expand(BaseModel):
        expand:list[MaleoAccessUserGeneralParameters.ExpandableFields] = Field([], description="Expanded field(s)")

    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"
        USERNAME = "username"
        EMAIL = "email"
        PHONE = "phone"

    class GetSingle(BaseGeneralParameters.GetSingle):
        identifier:MaleoAccessUserGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")
        value:Union[int, UUID, str] = Field(..., description="Value")

    class Update(BaseModel):
        user_type_id:int = Field(1, ge=1, description="User's type id")
        username:Optional[str] = Field(None, max_length=50, description="User's username")
        email:str = Field(..., max_length=255, description="User's email")
        phone:str = Field(..., max_length=15, description="User's phone")

    class Create(Update):
        password:str = Field(..., max_length=255, description="User's password")