from __future__ import annotations
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_organization_role import MaleoAccessUserOrganizationRoleGeneralParameters

class MaleoAccessUserOrganizationRoleServiceParameters:
    class GetQuery(
        MaleoAccessUserOrganizationRoleGeneralParameters.Get,
        BaseServiceParameters.GetQuery
    ): pass

    class Get(
        MaleoAccessUserOrganizationRoleGeneralParameters.Get,
        BaseServiceParameters.Get
    ): pass