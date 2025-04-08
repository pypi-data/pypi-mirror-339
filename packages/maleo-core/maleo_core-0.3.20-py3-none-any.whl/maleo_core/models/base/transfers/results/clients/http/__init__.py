# This file serves all HTTP Client's results

from __future__ import annotations
from .controller import BaseHTTPClientControllerResults
from .service import BaseHTTPClientServiceResults

class BaseHTTPClientResults:
    Controller = BaseHTTPClientControllerResults
    Service = BaseHTTPClientServiceResults

__all__ = ["BaseHTTPClientResults", "BaseHTTPClientControllerResults", "BaseHTTPClientServiceResults"]