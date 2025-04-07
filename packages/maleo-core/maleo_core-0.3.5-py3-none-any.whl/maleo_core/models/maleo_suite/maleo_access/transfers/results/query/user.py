from __future__ import annotations
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user import MaleoAccessUserGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_profile import MaleoAccessUserProfileGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.organization import MaleoAccessOrganizationQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.system_role import MaleoAccessSystemRoleQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_profile import MaleoAccessUserProfileQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_type import MaleoAccessUserTypeQueryResults

class MaleoAccessUserQueryResults:
    class UserSystemRole(MaleoAccessUserProfileGeneralTransfers.Base, BaseServiceQueryResults.Get):
        system_role:MaleoAccessSystemRoleQueryResults.Get = Field(..., description="System Role's data")

    class Get(MaleoAccessUserGeneralTransfers.Base, BaseServiceQueryResults.Get):
        user_type:MaleoAccessUserTypeQueryResults.Get = Field(..., description="User's type")
        profile:Optional[MaleoAccessUserProfileQueryResults.Get] = Field(None, description="User's profile")
        system_roles:list[MaleoAccessSystemRoleQueryResults.Get] = Field(..., description="User's system roles")
        users_system_roles:list[MaleoAccessUserQueryResults.UserSystemRole] = Field(..., description="Users system roles")
        organizations:list[MaleoAccessOrganizationQueryResults.Get] = Field(..., description="User's organizations")

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessUserQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessUserQueryResults.Get]