from __future__ import annotations
from maleo_core.models.base.transfers.results.clients.http.service import BaseHTTPClientServiceResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.organization import MaleoAccessOrganizationQueryResults

class MaleoAccessHTTPClientOrganizationServiceResults:
    Fail = BaseHTTPClientServiceResults.Fail

    class SingleChildData(BaseHTTPClientServiceResults.SingleData):
        data:MaleoAccessOrganizationQueryResults.GetChild

    class MultipleChildrenData(BaseHTTPClientServiceResults.MultipleData):
        data:list[MaleoAccessOrganizationQueryResults.GetChild]

    class SingleData(BaseHTTPClientServiceResults.SingleData):
        data:MaleoAccessOrganizationQueryResults.Get

    class MultipleData(BaseHTTPClientServiceResults.MultipleData):
        data:list[MaleoAccessOrganizationQueryResults.Get]