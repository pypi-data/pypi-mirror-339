from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user import MaleoAccessUserGeneralParameters

class MaleoAccessUserClientParameters:
    class Get(
        MaleoAccessUserGeneralParameters.Expand,
        MaleoAccessUserGeneralParameters.Get,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetQuery(
        MaleoAccessUserGeneralParameters.Expand,
        MaleoAccessUserGeneralParameters.Get,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass