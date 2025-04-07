from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization import MaleoAccessOrganizationGeneralParameters

class MaleoAccessOrganizationServiceParameters:
    class GetQuery(
        MaleoAccessOrganizationGeneralParameters.Expand,
        MaleoAccessOrganizationGeneralParameters.Get,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class Get(
        MaleoAccessOrganizationGeneralParameters.Expand,
        MaleoAccessOrganizationGeneralParameters.Get,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetChildrenQuery(
        MaleoAccessOrganizationGeneralParameters.ChildExpand,
        MaleoAccessOrganizationGeneralParameters.GetChildren,
        BaseServiceParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class GetChildren(
        MaleoAccessOrganizationGeneralParameters.ChildExpand,
        MaleoAccessOrganizationGeneralParameters.GetChildren,
        BaseServiceParameters.Get,
        BaseGeneralParameters.IDs
    ): pass