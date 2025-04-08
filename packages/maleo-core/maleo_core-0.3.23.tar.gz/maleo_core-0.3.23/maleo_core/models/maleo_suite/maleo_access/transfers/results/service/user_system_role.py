from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_system_role import MaleoAccessUserSystemRoleQueryResults

class MaleoAccessUserSystemRoleServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class SingleData(BaseServiceGeneralResults.SingleData):
        data:Optional[MaleoAccessUserSystemRoleQueryResults.Get]

    class MultipleData(BaseServiceGeneralResults.MultipleData):
        data:list[MaleoAccessUserSystemRoleQueryResults.Get]