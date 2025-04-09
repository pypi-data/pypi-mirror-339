from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_profile import MaleoAccessUserProfileGeneralTransfers

class MaleoAccessUserProfileGeneralParameters:
    class ExpandableFields(StrEnum):
        USER = "user"
        GENDER = "gender"
        BLOOD_TYPE = "blood_type"

    class Expand(BaseModel):
        expand:list[MaleoAccessUserProfileGeneralParameters.ExpandableFields] = Field([], description="Expanded field(s)")

    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"
        ID_CARD = "id_card"

    class GetSingle(Expand, BaseGeneralParameters.Statuses): pass

    class CreateOrUpdate(Expand, MaleoAccessUserProfileGeneralTransfers.Base): pass

    class StatusUpdate(Expand, BaseGeneralParameters.StatusUpdate): pass

    class UniqueFields(StrEnum):
        ID_CARD = "id_card"

    unique_field_nullability:dict[MaleoAccessUserProfileGeneralParameters.UniqueFields, bool] = {UniqueFields.ID_CARD: True}

    class UniqueFieldCheck(BaseGeneralParameters.UniqueFieldCheck):
        field:MaleoAccessUserProfileGeneralParameters.UniqueFields = Field(..., description="Field to be checked")

    UniqueFieldChecks = list[UniqueFieldCheck]

    @staticmethod
    def generate_unique_field_checks(
        operation:BaseGeneralParameters.OperationType,
        new_parameters:CreateOrUpdate,
        old_parameters:Optional[CreateOrUpdate]
    ) -> UniqueFieldChecks:
        return [
            MaleoAccessUserProfileGeneralParameters.UniqueFieldCheck(
                operation=operation,
                field=field,
                new_value=getattr(new_parameters, field.value),
                old_value=getattr(old_parameters, field.value) if operation == BaseGeneralParameters.OperationType.UPDATE else None,
                nullable=MaleoAccessUserProfileGeneralParameters.unique_field_nullability.get(field),
                suggestion=f"Select other {field} value{"" if not MaleoAccessUserProfileGeneralParameters.unique_field_nullability.get(field) else ", or set it to null"}."
            )
            for field in MaleoAccessUserProfileGeneralParameters.UniqueFields
        ]