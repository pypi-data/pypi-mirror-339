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

    class GetUser(
        MaleoAccessUserSystemRoleGeneralParameters.GetUser,
        BaseClientParameters.Get
    ): pass

    class GetUserQuery(
        MaleoAccessUserSystemRoleGeneralParameters.GetUser,
        BaseClientParameters.GetQuery
    ): pass

    class GetSystemRole(
        MaleoAccessUserSystemRoleGeneralParameters.GetSystemRole,
        BaseClientParameters.Get
    ): pass

    class GetSystemRoleQuery(
        MaleoAccessUserSystemRoleGeneralParameters.GetSystemRole,
        BaseClientParameters.GetQuery
    ): pass