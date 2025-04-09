from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_organization_role import MaleoAccessUserOrganizationRoleGeneralTransfers

class MaleoAccessUserOrganizationRoleGeneralParameters:
    class ExpandableFields(StrEnum):
        USER_ORGANIZATION = "user_organization"
        ORGANIZATION_ROLE = "organization_role"

    class Expand(BaseModel):
        expand:list[MaleoAccessUserOrganizationRoleGeneralParameters.ExpandableFields] = Field([], description="Expanded field(s)")

    class BaseGet(BaseModel):
        organization_role_ids:Optional[list[int]] = Field(None, description="Organization roles id's")

    class Get(Expand, BaseGet): pass

    class GetSingle(Expand, BaseGeneralParameters.Statuses): pass

    class Create(Expand, MaleoAccessUserOrganizationRoleGeneralTransfers.Base): pass

    class StatusUpdate(Expand, BaseGeneralParameters.StatusUpdate): pass