from __future__ import annotations
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_system_role import MaleoAccessUserSystemRoleGeneralParameters

class MaleoAccessUserSystemRoleServiceParameters:
    class GetQuery(
        MaleoAccessUserSystemRoleGeneralParameters.Get,
        BaseServiceParameters.GetQuery
    ): pass

    class Get(
        MaleoAccessUserSystemRoleGeneralParameters.Get,
        BaseServiceParameters.Get
    ): pass

    class GetSystemRoleQuery(
        MaleoAccessUserSystemRoleGeneralParameters.GetSystemRole,
        BaseServiceParameters.GetQuery
    ): pass

    class GetSystemRole(
        MaleoAccessUserSystemRoleGeneralParameters.GetSystemRole,
        BaseServiceParameters.Get
    ): pass

    class GetUserQuery(
        MaleoAccessUserSystemRoleGeneralParameters.GetUser,
        BaseServiceParameters.GetQuery
    ): pass

    class GetUser(
        MaleoAccessUserSystemRoleGeneralParameters.GetUser,
        BaseServiceParameters.Get
    ): pass