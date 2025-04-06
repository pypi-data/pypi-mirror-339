from __future__ import annotations
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization import MaleoAccessOrganizationGeneralParameters

class MaleoAccessOrganizationClientParameters:
    class Get(
        MaleoAccessOrganizationGeneralParameters.Expand,
        BaseClientParameters.Get,
        MaleoAccessOrganizationGeneralParameters.Get
    ): pass
    class GetQuery(
        MaleoAccessOrganizationGeneralParameters.Expand,
        BaseClientParameters.GetQuery,
        MaleoAccessOrganizationGeneralParameters.Get
    ): pass