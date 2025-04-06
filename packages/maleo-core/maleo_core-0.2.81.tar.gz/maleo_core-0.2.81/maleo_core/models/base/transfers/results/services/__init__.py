# This file serves all base services results

from __future__ import annotations
from .general import BaseServiceGeneralResults
from .controllers import BaseServiceControllerResults
from .query import BaseServiceQueryResults

class BaseServiceResults:
    General = BaseServiceGeneralResults
    Controller = BaseServiceControllerResults
    Query = BaseServiceQueryResults

__all__ = ["BaseServiceResults", "BaseServiceGeneralResults", "BaseServiceControllerResults", "BaseServiceQueryResults"]