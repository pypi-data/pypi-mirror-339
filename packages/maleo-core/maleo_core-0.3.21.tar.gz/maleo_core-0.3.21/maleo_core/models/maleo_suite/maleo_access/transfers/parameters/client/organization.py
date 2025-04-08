from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization import MaleoAccessOrganizationGeneralParameters

class MaleoAccessOrganizationClientParameters:
    class Get(
        MaleoAccessOrganizationGeneralParameters.Get,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetQuery(
        MaleoAccessOrganizationGeneralParameters.Get,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass

    class GetChildren(
        MaleoAccessOrganizationGeneralParameters.GetChildren,
        BaseClientParameters.Get,
        BaseGeneralParameters.IDs
    ): pass

    class GetChildrenQuery(
        MaleoAccessOrganizationGeneralParameters.GetChildren,
        BaseClientParameters.GetQuery,
        BaseGeneralParameters.IDs
    ): pass