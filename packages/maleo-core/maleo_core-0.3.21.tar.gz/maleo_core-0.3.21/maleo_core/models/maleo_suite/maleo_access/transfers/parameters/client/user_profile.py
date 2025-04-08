from __future__ import annotations
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_profile import MaleoAccessUserProfileGeneralParameters

class MaleoAccessUserProfileClientParameters:
    class Get(
        MaleoAccessUserProfileGeneralParameters.Expand,
        BaseClientParameters.Get
    ): pass

    class GetQuery(
        MaleoAccessUserProfileGeneralParameters.Expand,
        BaseClientParameters.GetQuery
    ): pass