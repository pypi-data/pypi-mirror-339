# This file serves all base service's controller results

from __future__ import annotations
from .rest import BaseServiceRESTControllerResults

class BaseServiceControllerResults:
    REST = BaseServiceRESTControllerResults

__all__ = ["BaseServiceControllerResults", "BaseServiceRESTControllerResults"]