from __future__ import annotations
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_profile import MaleoAccessUserProfileGeneralParameters

class MaleoAccessUserProfileServiceParameters:
    class GetQuery(
        MaleoAccessUserProfileGeneralParameters.Expand,
        BaseServiceParameters.GetQuery
    ): pass

    class Get(
        MaleoAccessUserProfileGeneralParameters.Expand,
        BaseServiceParameters.Get
    ): pass