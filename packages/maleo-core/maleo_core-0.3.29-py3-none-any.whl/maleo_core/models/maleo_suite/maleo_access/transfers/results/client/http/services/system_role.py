from __future__ import annotations
from maleo_core.models.base.transfers.results.clients.http.service import BaseHTTPClientServiceResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.system_role import MaleoAccessSystemRoleQueryResults

class MaleoAccessHTTPClientSystemRoleServiceResults:
    Fail = BaseHTTPClientServiceResults.Fail

    class SingleData(BaseHTTPClientServiceResults.SingleData):
        data:MaleoAccessSystemRoleQueryResults.Get

    class MultipleData(BaseHTTPClientServiceResults.MultipleData):
        data:list[MaleoAccessSystemRoleQueryResults.Get]