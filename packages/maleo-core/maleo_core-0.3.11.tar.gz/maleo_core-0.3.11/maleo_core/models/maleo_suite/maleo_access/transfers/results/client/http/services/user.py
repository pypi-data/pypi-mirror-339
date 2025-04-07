from __future__ import annotations
from maleo_core.models.base.transfers.results.clients.http.service import BaseHTTPClientServiceResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user import MaleoAccessUserQueryResults

class MaleoAccessHTTPClientUserServiceResults:
    Fail = BaseHTTPClientServiceResults.Fail

    class SingleData(BaseHTTPClientServiceResults.SingleData):
        data:MaleoAccessUserQueryResults.Get

    class MultipleData(BaseHTTPClientServiceResults.MultipleData):
        data:list[MaleoAccessUserQueryResults.Get]