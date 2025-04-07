# This file serves all MaleoShared's Client Results

from __future__ import annotations
from .http import MaleoSharedHTTPClientResults

class MaleoSharedClientResults:
    HTTP = MaleoSharedHTTPClientResults

__all__ = ["MaleoSharedClientResults", "MaleoSharedHTTPClientResults"]