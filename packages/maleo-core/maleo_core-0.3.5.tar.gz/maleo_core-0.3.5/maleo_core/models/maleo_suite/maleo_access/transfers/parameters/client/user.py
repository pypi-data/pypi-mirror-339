from __future__ import annotations
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user import MaleoAccessUserGeneralParameters

class MaleoAccessUserClientParameters:
    class Get(
        MaleoAccessUserGeneralParameters.Expand,
        MaleoAccessUserGeneralParameters.Get,
        BaseClientParameters.Get
    ): pass

    class GetQuery(
        MaleoAccessUserGeneralParameters.Expand,
        MaleoAccessUserGeneralParameters.Get,
        BaseClientParameters.GetQuery
    ): pass