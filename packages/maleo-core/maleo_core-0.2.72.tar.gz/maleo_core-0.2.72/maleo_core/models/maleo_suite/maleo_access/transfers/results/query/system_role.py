from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.system_role import MaleoAccessSystemRoleGeneralTransfers

class MaleoAccessSystemRoleQueryResults:
    class Get(MaleoAccessSystemRoleGeneralTransfers.Base, BaseServiceQueryResults.Get): pass

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessSystemRoleQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessSystemRoleQueryResults.Get]