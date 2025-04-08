from __future__ import annotations
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_organization import MaleoAccessUserOrganizationGeneralParameters

class MaleoAccessUserOrganizationServiceParameters:
    class GetQuery(
        MaleoAccessUserOrganizationGeneralParameters.Get,
        BaseServiceParameters.GetQuery
    ): pass

    class Get(
        MaleoAccessUserOrganizationGeneralParameters.Get,
        BaseServiceParameters.Get
    ): pass

    class GetOrganizationQuery(
        MaleoAccessUserOrganizationGeneralParameters.GetOrganization,
        BaseServiceParameters.GetQuery
    ): pass

    class GetOrganization(
        MaleoAccessUserOrganizationGeneralParameters.GetOrganization,
        BaseServiceParameters.Get
    ): pass

    class GetUserQuery(
        MaleoAccessUserOrganizationGeneralParameters.GetUser,
        BaseServiceParameters.GetQuery
    ): pass

    class GetUser(
        MaleoAccessUserOrganizationGeneralParameters.GetUser,
        BaseServiceParameters.Get
    ): pass