from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_type import MaleoAccessUserTypeGeneralTransfers

class MaleoAccessUserTypeQueryResults:
    class Get(MaleoAccessUserTypeGeneralTransfers.Base, BaseServiceQueryResults.Get): pass

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessUserTypeQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessUserTypeQueryResults.Get]