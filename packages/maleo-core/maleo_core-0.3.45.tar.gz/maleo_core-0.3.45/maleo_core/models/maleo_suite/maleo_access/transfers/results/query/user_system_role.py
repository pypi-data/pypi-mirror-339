from __future__ import annotations
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_system_role import MaleoAccessUserSystemRoleGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.system_role import MaleoAccessSystemRoleQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user import MaleoAccessUserQueryResults

class MaleoAccessUserSystemRoleQueryResults:
    class Get(MaleoAccessUserSystemRoleGeneralTransfers.Base, BaseServiceQueryResults.Get):
        user:MaleoAccessUserQueryResults.BaseGet = Field(..., description="User's data")
        system_role:MaleoAccessSystemRoleQueryResults.Get = Field(..., description="System Role's data")

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessUserSystemRoleQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessUserSystemRoleQueryResults.Get]