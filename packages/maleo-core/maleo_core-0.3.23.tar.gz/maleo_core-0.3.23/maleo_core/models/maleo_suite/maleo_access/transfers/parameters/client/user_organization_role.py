from __future__ import annotations
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_organization_role import MaleoAccessUserOrganizationRoleGeneralParameters

class MaleoAccessUserOrganizationRoleClientParameters:
    class Get(
        MaleoAccessUserOrganizationRoleGeneralParameters.Get,
        BaseClientParameters.Get
    ): pass

    class GetQuery(
        MaleoAccessUserOrganizationRoleGeneralParameters.Get,
        BaseClientParameters.GetQuery
    ): pass