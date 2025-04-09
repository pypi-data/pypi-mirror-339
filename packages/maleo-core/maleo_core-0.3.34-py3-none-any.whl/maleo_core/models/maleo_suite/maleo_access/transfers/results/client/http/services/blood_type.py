from __future__ import annotations
from maleo_core.models.base.transfers.results.clients.http.service import BaseHTTPClientServiceResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.blood_type import MaleoAccessBloodTypeQueryResults

class MaleoAccessHTTPClientBloodTypeServiceResults:
    Fail = BaseHTTPClientServiceResults.Fail

    class SingleData(BaseHTTPClientServiceResults.SingleData):
        data:MaleoAccessBloodTypeQueryResults.Get

    class MultipleData(BaseHTTPClientServiceResults.MultipleData):
        data:list[MaleoAccessBloodTypeQueryResults.Get]