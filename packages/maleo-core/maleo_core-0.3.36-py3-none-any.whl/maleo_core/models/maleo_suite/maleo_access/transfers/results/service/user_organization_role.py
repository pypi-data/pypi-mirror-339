from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_organization_role import MaleoAccessUserOrganizationRoleQueryResults

class MaleoAccessUserOrganizationRoleServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class SingleData(BaseServiceGeneralResults.SingleData):
        data:Optional[MaleoAccessUserOrganizationRoleQueryResults.Get]

    class MultipleData(BaseServiceGeneralResults.MultipleData):
        data:list[MaleoAccessUserOrganizationRoleQueryResults.Get]