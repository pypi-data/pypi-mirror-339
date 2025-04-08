# This file serves all client's results

from __future__ import annotations
from .http import BaseHTTPClientResults

class BaseClientResults:
    HTTP = BaseHTTPClientResults

__all__ = ["ClientResults", "BaseHTTPClientResults"]