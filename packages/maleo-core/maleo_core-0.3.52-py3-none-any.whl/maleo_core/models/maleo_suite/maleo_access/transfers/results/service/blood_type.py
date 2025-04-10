from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.blood_type import MaleoAccessBloodTypeQueryResults

class MaleoAccessBloodTypeServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class SingleData(BaseServiceGeneralResults.SingleData):
        data:Optional[MaleoAccessBloodTypeQueryResults.Get]

    class MultipleData(BaseServiceGeneralResults.MultipleData):
        data:list[MaleoAccessBloodTypeQueryResults.Get]