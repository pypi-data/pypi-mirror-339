from __future__ import annotations
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user import MaleoAccessUserGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_organization import MaleoAccessUserOrganizationGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_system_role import MaleoAccessUserSystemRoleGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.organization import MaleoAccessOrganizationQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.system_role import MaleoAccessSystemRoleQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_profile import MaleoAccessUserProfileQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_type import MaleoAccessUserTypeQueryResults

class MaleoAccessUserQueryResults:
    class UserOrganization(MaleoAccessUserOrganizationGeneralTransfers.Base, BaseServiceQueryResults.Get):
        organization:MaleoAccessOrganizationQueryResults.Get = Field(..., description="Organization's data")

    class UserSystemRole(MaleoAccessUserSystemRoleGeneralTransfers.Base, BaseServiceQueryResults.Get):
        system_role:MaleoAccessSystemRoleQueryResults.Get = Field(..., description="System Role's data")

    class BaseGet(MaleoAccessUserGeneralTransfers.Base, BaseServiceQueryResults.Get): pass

    class Get(BaseGet):
        user_type:MaleoAccessUserTypeQueryResults.Get = Field(..., description="User's type")
        profile:Optional[MaleoAccessUserProfileQueryResults.Get] = Field(None, description="User's profile")
        # system_roles:list[MaleoAccessSystemRoleQueryResults.Get] = Field(..., description="User's system roles")
        # users_system_roles:list[MaleoAccessUserQueryResults.UserSystemRole] = Field(..., description="Users system roles")
        # organizations:list[MaleoAccessOrganizationQueryResults.Get] = Field(..., description="User's organizations")
        # users_organizations:list[MaleoAccessUserQueryResults.UserOrganization] = Field(..., description="Users organizations")

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessUserQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessUserQueryResults.Get]