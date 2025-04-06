from __future__ import annotations
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization import MaleoAccessOrganizationGeneralParameters

class MaleoAccessOrganizationServiceParameters:
    class GetQuery(
        MaleoAccessOrganizationGeneralParameters.Expand,
        BaseServiceParameters.GetQuery,
        MaleoAccessOrganizationGeneralParameters.Get
    ): pass
    class Get(
        MaleoAccessOrganizationGeneralParameters.Expand,
        BaseServiceParameters.Get,
        MaleoAccessOrganizationGeneralParameters.Get
    ): pass