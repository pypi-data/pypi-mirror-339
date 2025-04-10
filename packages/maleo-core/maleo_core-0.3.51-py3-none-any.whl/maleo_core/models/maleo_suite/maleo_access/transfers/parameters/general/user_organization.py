from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_organization import MaleoAccessUserOrganizationGeneralTransfers

class MaleoAccessUserOrganizationGeneralParameters:
    class ExpandableFields(StrEnum):
        USER = "user"
        ORGANIZATION = "organization"

    class Expand(BaseModel):
        expand:list[MaleoAccessUserOrganizationGeneralParameters.ExpandableFields] = Field([], description="Expanded field(s)")

    class BaseGet(BaseModel):
        user_ids:Optional[list[int]] = Field(None, description="Users id's")
        organization_ids:Optional[list[int]] = Field(None, description="Organizations id's")

    class Get(Expand, BaseGet): pass

    class GetSingle(Expand, BaseGeneralParameters.Statuses): pass

    class Create(Expand, MaleoAccessUserOrganizationGeneralTransfers.Base): pass

    class StatusUpdate(Expand, BaseGeneralParameters.StatusUpdate): pass

    class BaseGetUser(BaseModel):
        user_ids:Optional[list[int]] = Field(None, description="Users id's")

    class GetUser(Expand, BaseGetUser): pass

    class BaseGetOrganization(BaseModel):
        organization_ids:Optional[list[int]] = Field(None, description="Organizations id's")

    class GetOrganization(Expand, BaseGetOrganization): pass