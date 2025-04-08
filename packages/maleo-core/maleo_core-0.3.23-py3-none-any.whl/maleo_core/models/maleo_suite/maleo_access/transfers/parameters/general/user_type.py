from __future__ import annotations
from enum import StrEnum
from pydantic import Field
from typing import Optional, Union
from uuid import UUID
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_type import MaleoAccessUserTypeGeneralTransfers

class MaleoAccessUserTypeGeneralParameters:
    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"
        KEY = "key"
        NAME = "name"

    class GetSingle(BaseGeneralParameters.GetSingle):
        identifier:MaleoAccessUserTypeGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")
        value:Union[int, UUID, str] = Field(..., description="Value")

    CreateOrUpdate = MaleoAccessUserTypeGeneralTransfers.Base

    class UniqueFields(StrEnum):
        KEY = "key"
        NAME = "name"

    unique_field_nullability:dict[
        MaleoAccessUserTypeGeneralParameters.UniqueFields,
        bool
    ] = {
        UniqueFields.KEY: False,
        UniqueFields.NAME: False
    }

    class UniqueFieldCheck(BaseGeneralParameters.UniqueFieldCheck):
        field:MaleoAccessUserTypeGeneralParameters.UniqueFields = Field(..., description="Field to be checked")

    UniqueFieldChecks = list[UniqueFieldCheck]

    @staticmethod
    def generate_unique_field_checks(
        operation:BaseGeneralParameters.OperationType,
        new_parameters:CreateOrUpdate,
        old_parameters:Optional[CreateOrUpdate]
    ) -> UniqueFieldChecks:
        update_unique_field_checks = [
            MaleoAccessUserTypeGeneralParameters.UniqueFieldCheck(
                operation=operation,
                field=field,
                new_value=getattr(new_parameters, field.value),
                old_value=getattr(old_parameters, field.value) if operation == BaseGeneralParameters.OperationType.UPDATE else None,
                nullable=MaleoAccessUserTypeGeneralParameters.unique_field_nullability.get(field),
                suggestion=f"Select other {field} value{"" if not MaleoAccessUserTypeGeneralParameters.unique_field_nullability.get(field) else ", or set it to null"}."
            )
            for field in MaleoAccessUserTypeGeneralParameters.UniqueFields
        ]
        return update_unique_field_checks