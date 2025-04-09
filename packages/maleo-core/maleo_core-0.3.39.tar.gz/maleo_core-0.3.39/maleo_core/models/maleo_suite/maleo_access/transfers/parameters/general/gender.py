from __future__ import annotations
from enum import StrEnum
from pydantic import Field
from typing import Optional, Union
from uuid import UUID
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.general.gender import MaleoAccessGenderGeneralTransfers

class MaleoAccessGenderGeneralParameters:
    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"
        KEY = "key"
        NAME = "name"

    class GetSingle(BaseGeneralParameters.GetSingle):
        identifier:MaleoAccessGenderGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")
        value:Union[int, UUID, str] = Field(..., description="Value")

    CreateOrUpdate = MaleoAccessGenderGeneralTransfers.Base

    class UniqueFields(StrEnum):
        KEY = "key"
        NAME = "name"

    unique_field_nullability:dict[
        MaleoAccessGenderGeneralParameters.UniqueFields,
        bool
    ] = {
        UniqueFields.KEY: False,
        UniqueFields.NAME: False
    }

    class UniqueFieldCheck(BaseGeneralParameters.UniqueFieldCheck):
        field:MaleoAccessGenderGeneralParameters.UniqueFields = Field(..., description="Field to be checked")

    UniqueFieldChecks = list[UniqueFieldCheck]

    @staticmethod
    def generate_unique_field_checks(
        operation:BaseGeneralParameters.OperationType,
        new_parameters:CreateOrUpdate,
        old_parameters:Optional[CreateOrUpdate]
    ) -> UniqueFieldChecks:
        update_unique_field_checks = [
            MaleoAccessGenderGeneralParameters.UniqueFieldCheck(
                operation=operation,
                field=field,
                new_value=getattr(new_parameters, field.value),
                old_value=getattr(old_parameters, field.value) if operation == BaseGeneralParameters.OperationType.UPDATE else None,
                nullable=MaleoAccessGenderGeneralParameters.unique_field_nullability.get(field),
                suggestion=f"Select other {field} value{"" if not MaleoAccessGenderGeneralParameters.unique_field_nullability.get(field) else ", or set it to null"}."
            )
            for field in MaleoAccessGenderGeneralParameters.UniqueFields
        ]
        return update_unique_field_checks