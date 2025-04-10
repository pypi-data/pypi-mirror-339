from __future__ import annotations
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_organization import MaleoAccessUserOrganizationGeneralParameters

class MaleoAccessUserOrganizationClientParameters:
    class Get(
        MaleoAccessUserOrganizationGeneralParameters.Get,
        BaseClientParameters.Get
    ): pass

    class GetQuery(
        MaleoAccessUserOrganizationGeneralParameters.Get,
        BaseClientParameters.GetQuery
    ): pass

    class GetUser(
        MaleoAccessUserOrganizationGeneralParameters.GetUser,
        BaseClientParameters.Get
    ): pass

    class GetUserQuery(
        MaleoAccessUserOrganizationGeneralParameters.GetUser,
        BaseClientParameters.GetQuery
    ): pass

    class GetOrganization(
        MaleoAccessUserOrganizationGeneralParameters.GetOrganization,
        BaseClientParameters.Get
    ): pass

    class GetOrganizationQuery(
        MaleoAccessUserOrganizationGeneralParameters.GetOrganization,
        BaseClientParameters.GetQuery
    ): pass