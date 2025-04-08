from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.gender import MaleoAccessGenderGeneralTransfers

class MaleoAccessGenderQueryResults:
    class Get(MaleoAccessGenderGeneralTransfers.Base, BaseServiceQueryResults.Get): pass

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessGenderQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessGenderQueryResults.Get]