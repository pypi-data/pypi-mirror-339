from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional, Union
from uuid import UUID
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.general.organization import MaleoAccessOrganizationGeneralTransfers

class MaleoAccessOrganizationGeneralParameters:
    class ExpandableFields(StrEnum):
        TYPE = "organization_type"
        PARENT = "parent_organization"
        CHILD = "child_organizations"

    expandable_fields:set[ExpandableFields] = {
        ExpandableFields.TYPE,
        ExpandableFields.PARENT,
        ExpandableFields.CHILD
    }

    class Expand(BaseModel):
        expand:list[MaleoAccessOrganizationGeneralParameters.ExpandableFields] = Field([], description="Expanded field(s)")

    class Get(BaseModel):
        is_root:Optional[bool] = Field(None, description="Filter organizations based on whether it's a root.")
        is_parent:Optional[bool] = Field(None, description="Filter organizations based on whether it's a parent.")
        is_child:Optional[bool] = Field(None, description="Filter organizations based on whether it's a child.")
        is_leaf:Optional[bool] = Field(None, description="Filter organizations based on whether it's a leaf.")

    class UniqueIdentifiers(StrEnum):
        ID = "id"
        UUID = "uuid"
        KEY = "key"

    class GetSingle(Expand, BaseGeneralParameters.GetSingle):
        identifier:MaleoAccessOrganizationGeneralParameters.UniqueIdentifiers = Field(..., description="Identifier")
        value:Union[int, UUID, str] = Field(..., description="Value")

    class GetSingleQuery(Expand, BaseGeneralParameters.GetSingleQuery): pass

    class CreateOrUpdate(Expand, MaleoAccessOrganizationGeneralTransfers.Base): pass

    class StatusUpdate(Expand, BaseGeneralParameters.StatusUpdate): pass

    class UniqueFields(StrEnum):
        KEY = "key"

    unique_field_nullability:dict[MaleoAccessOrganizationGeneralParameters.UniqueFields, bool] = {UniqueFields.KEY: False}

    class UniqueFieldCheck(BaseGeneralParameters.UniqueFieldCheck):
        field:MaleoAccessOrganizationGeneralParameters.UniqueFields = Field(..., description="Field to be checked")

    UniqueFieldChecks = list[UniqueFieldCheck]

    @staticmethod
    def generate_unique_field_checks(
        operation:BaseGeneralParameters.OperationType,
        new_parameters:CreateOrUpdate,
        old_parameters:Optional[CreateOrUpdate]
    ) -> UniqueFieldChecks:
        return [
            MaleoAccessOrganizationGeneralParameters.UniqueFieldCheck(
                operation=operation,
                field=field,
                new_value=getattr(new_parameters, field.value),
                old_value=getattr(old_parameters, field.value) if operation == BaseGeneralParameters.OperationType.UPDATE else None,
                nullable=MaleoAccessOrganizationGeneralParameters.unique_field_nullability.get(field),
                suggestion=f"Select other {field} value{"" if not MaleoAccessOrganizationGeneralParameters.unique_field_nullability.get(field) else ", or set it to null"}."
            )
            for field in MaleoAccessOrganizationGeneralParameters.UniqueFields
        ]