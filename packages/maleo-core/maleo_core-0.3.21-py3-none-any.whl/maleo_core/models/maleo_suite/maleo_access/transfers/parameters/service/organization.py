from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization import MaleoAccessOrganizationGeneralParameters

class MaleoAccessOrganizationServiceParameters:
    class GetQuery(
        MaleoAccessOrganizationGeneralParameters.Get,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class Get(
        MaleoAccessOrganizationGeneralParameters.Get,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetChildrenQuery(
        MaleoAccessOrganizationGeneralParameters.GetChildren,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class GetChildren(
        MaleoAccessOrganizationGeneralParameters.GetChildren,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass