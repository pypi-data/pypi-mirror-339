from __future__ import annotations
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_system_role import MaleoAccessUserSystemRoleGeneralParameters

class MaleoAccessUserSystemRoleClientParameters:
    class Get(
        MaleoAccessUserSystemRoleGeneralParameters.Get,
        BaseClientParameters.Get
    ): pass

    class GetQuery(
        MaleoAccessUserSystemRoleGeneralParameters.Get,
        BaseClientParameters.GetQuery
    ): pass