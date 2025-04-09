from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.organization_role import MaleoAccessOrganizationRoleGeneralTransfers

class MaleoAccessOrganizationRoleQueryResults:
    class Get(MaleoAccessOrganizationRoleGeneralTransfers.Base, BaseServiceQueryResults.Get): pass

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessOrganizationRoleQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessOrganizationRoleQueryResults.Get]