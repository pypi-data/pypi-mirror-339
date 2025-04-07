from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.organization import MaleoAccessOrganizationQueryResults

class MaleoAccessOrganizationServiceResults:
    Fail = BaseServiceGeneralResults.Fail

    class SingleChildData(BaseServiceGeneralResults.SingleData):
        data:Optional[MaleoAccessOrganizationQueryResults.GetChild]

    class MultipleChildrenData(BaseServiceGeneralResults.MultipleData):
        data:list[MaleoAccessOrganizationQueryResults.GetChild]

    class SingleData(BaseServiceGeneralResults.SingleData):
        data:Optional[MaleoAccessOrganizationQueryResults.Get]

    class MultipleData(BaseServiceGeneralResults.MultipleData):
        data:list[MaleoAccessOrganizationQueryResults.Get]