from __future__ import annotations
from maleo_core.models.base.transfers.results.clients.http.service import BaseHTTPClientServiceResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_organization import MaleoAccessUserOrganizationQueryResults

class MaleoAccessHTTPClientUserOrganizationServiceResults:
    Fail = BaseHTTPClientServiceResults.Fail

    class SingleData(BaseHTTPClientServiceResults.SingleData):
        data:MaleoAccessUserOrganizationQueryResults.Get

    class MultipleData(BaseHTTPClientServiceResults.MultipleData):
        data:list[MaleoAccessUserOrganizationQueryResults.Get]