from __future__ import annotations
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.organization_type import MaleoAccessOrganizationTypeGeneralTransfers

class MaleoAccessOrganizationTypeQueryResults:
    class Get(MaleoAccessOrganizationTypeGeneralTransfers.Base, BaseServiceQueryResults.Get): pass

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessOrganizationTypeQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessOrganizationTypeQueryResults.Get]