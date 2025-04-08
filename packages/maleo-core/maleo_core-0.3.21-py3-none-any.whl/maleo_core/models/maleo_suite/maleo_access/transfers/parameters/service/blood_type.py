from __future__ import annotations
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.parameters.service import BaseServiceParameters

class MaleoAccessBloodTypeServiceParameters:
    class GetQuery(BaseServiceParameters.GetQuery, BaseGeneralParameters.IDs): pass
    class Get(BaseServiceParameters.Get, BaseGeneralParameters.IDs): pass