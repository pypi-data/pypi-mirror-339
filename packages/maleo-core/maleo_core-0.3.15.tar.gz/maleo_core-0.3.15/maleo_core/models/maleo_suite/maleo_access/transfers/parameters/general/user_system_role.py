from __future__ import annotations
from enum import StrEnum
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_system_role import MaleoAccessUserSystemRoleGeneralTransfers

class MaleoAccessUserSystemRoleGeneralParameters:
    class ExpandableFields(StrEnum):
        USER = "user"
        SYSTEM_ROLE = "system_role"

    class Expand(BaseModel):
        expand:list[MaleoAccessUserSystemRoleGeneralParameters.ExpandableFields] = Field([], description="Expanded field(s)")

    class BaseGet(BaseModel):
        user_ids:Optional[list[int]] = Field(None, description="Users id's")
        system_role_ids:Optional[list[int]] = Field(None, description="System roles id's")

    class Get(Expand, BaseGet): pass

    class GetSingle(Expand, BaseGeneralParameters.Statuses, MaleoAccessUserSystemRoleGeneralTransfers.Base): pass

    class Create(Expand, MaleoAccessUserSystemRoleGeneralTransfers.Base): pass

    class StatusUpdate(Expand, BaseGeneralParameters.StatusUpdate): pass

    class GetUserExpandableFields(StrEnum):
        SYSTEM_ROLE = "system_role"

    class GetUserExpand(BaseModel):
        expand:list[MaleoAccessUserSystemRoleGeneralParameters.GetUserExpandableFields] = Field([], description="Expanded field(s)")

    class BaseGetUser(BaseModel):
        user_ids:Optional[list[int]] = Field(None, description="Users id's")

    class GetUser(GetUserExpand, BaseGetUser): pass

    class GetSystemRoleExpandableFields(StrEnum):
        USER = "user"

    class GetSystemRoleExpand(BaseModel):
        expand:list[MaleoAccessUserSystemRoleGeneralParameters.GetSystemRoleExpandableFields] = Field([], description="Expanded field(s)")

    class BaseGetSystemRole(BaseModel):
        system_role_ids:Optional[list[int]] = Field(None, description="System roles id's")

    class GetSystemRole(GetSystemRoleExpand, BaseGetSystemRole): pass