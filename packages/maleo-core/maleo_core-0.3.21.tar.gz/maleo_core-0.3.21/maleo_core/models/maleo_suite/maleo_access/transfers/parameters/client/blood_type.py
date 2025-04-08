from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.client import BaseClientParameters

class MaleoAccessBloodTypeClientParameters:
    class Get(BaseClientParameters.Get, BaseGeneralParameters.IDs): pass
    class GetQuery(BaseClientParameters.GetQuery, BaseGeneralParameters.IDs): pass