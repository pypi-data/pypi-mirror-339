from __future__ import annotations
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user import MaleoAccessUserGeneralParameters

class MaleoAccessUserServiceParameters:
    class GetQuery(
        MaleoAccessUserGeneralParameters.Expand,
        MaleoAccessUserGeneralParameters.Get,
        BaseServiceParameters.GetQuery
    ): pass

    class Get(
        MaleoAccessUserGeneralParameters.Expand,
        MaleoAccessUserGeneralParameters.Get,
        BaseServiceParameters.Get
    ): pass