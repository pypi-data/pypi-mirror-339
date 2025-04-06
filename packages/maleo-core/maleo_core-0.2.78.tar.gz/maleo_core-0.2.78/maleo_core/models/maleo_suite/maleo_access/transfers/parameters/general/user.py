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

    class Expand(BaseModel):
        expand:list[MaleoAccessUserGeneralParameters.ExpandableFields] = Field([], description="Expanded field(s)")

    class UserTypeIDs(BaseModel):
        user_type_ids:Optional[list[int]] = Field(None, description="Specific user type IDs")

    class Get(UserTypeIDs): pass

    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"
        USERNAME = "username"
        EMAIL = "email"
        PHONE = "phone"

    class GetSingle(Expand, BaseGeneralParameters.GetSingle):
        identifier:MaleoAccessUserGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")
        value:Union[int, UUID, str] = Field(..., description="Value")

    class GetSingleQuery(Expand, BaseGeneralParameters.GetSingleQuery): pass

    class BaseUpdate(BaseModel):
        username:Optional[str] = Field(None, max_length=50, description="User's username")
        email:str = Field(..., max_length=255, description="User's email")
        phone:str = Field(..., max_length=15, description="User's phone")
        user_type_id:int = Field(1, ge=1, description="User's type id")

    class Update(Expand, BaseUpdate): pass

    class BaseCreate(BaseUpdate):
        password:str = Field(..., max_length=255, description="User's password")

    class Create(Expand, BaseCreate): pass

    class StatusUpdate(Expand, BaseGeneralParameters.StatusUpdate): pass

    class UniqueFields(StrEnum):
        USERNAME = "username"
        EMAIL = "email"
        PHONE = "phone"

    unique_field_nullability:dict[MaleoAccessUserGeneralParameters.UniqueFields, bool] = {
        UniqueFields.USERNAME: True,
        UniqueFields.EMAIL: False,
        UniqueFields.PHONE: False
    }

    class UniqueFieldCheck(BaseGeneralParameters.UniqueFieldCheck):
        field:MaleoAccessUserGeneralParameters.UniqueFields = Field(..., description="Field to be checked")

    UniqueFieldChecks = list[UniqueFieldCheck]

    @staticmethod
    def generate_unique_field_checks(
        operation:BaseGeneralParameters.OperationType,
        new_parameters:BaseUpdate,
        old_parameters:Optional[BaseUpdate]
    ) -> UniqueFieldChecks:
        return [
            MaleoAccessUserGeneralParameters.UniqueFieldCheck(
                operation=operation,
                field=field,
                new_value=getattr(new_parameters, field.value),
                old_value=getattr(old_parameters, field.value) if operation == BaseGeneralParameters.OperationType.UPDATE else None,
                nullable=MaleoAccessUserGeneralParameters.unique_field_nullability.get(field),
                suggestion=f"Select other {field} value{"" if not MaleoAccessUserGeneralParameters.unique_field_nullability.get(field) else ", or set it to null"}."
            )
            for field in MaleoAccessUserGeneralParameters.UniqueFields
        ]