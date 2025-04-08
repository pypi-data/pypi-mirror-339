from __future__ import annotations
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_organization_role import MaleoAccessUserOrganizationRoleGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_organization import MaleoAccessUserOrganizationQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.organization_role import MaleoAccessOrganizationRoleQueryResults

class MaleoAccessUserOrganizationRoleQueryResults:
    class Get(MaleoAccessUserOrganizationRoleGeneralTransfers.Base, BaseServiceQueryResults.Get):
        user_organization:MaleoAccessUserOrganizationQueryResults.Get = Field(..., description="User organization's data")
        organization_role:MaleoAccessOrganizationRoleQueryResults.Get = Field(..., description="Organization role's data")

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessUserOrganizationRoleQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessUserOrganizationRoleQueryResults.Get]