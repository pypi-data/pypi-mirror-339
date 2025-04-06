# This file serves all MaleoAccess's Client Results

from __future__ import annotations
from .http import MaleoAccessHTTPClientResults

class MaleoAccessClientResults:
    HTTP = MaleoAccessHTTPClientResults

__all__ = ["MaleoAccessClientResults", "MaleoAccessHTTPClientResults"]