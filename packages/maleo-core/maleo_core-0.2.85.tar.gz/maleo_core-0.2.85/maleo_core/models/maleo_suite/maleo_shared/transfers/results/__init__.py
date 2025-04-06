# This file serves all MaleoShared's Results

from __future__ import annotations
from .client import MaleoSharedClientResults
from .service import MaleoSharedServiceResults
from .query import MaleoSharedQueryResults

class MaleoSharedResults:
    Client = MaleoSharedClientResults
    Service = MaleoSharedServiceResults
    Query = MaleoSharedQueryResults

__all__ = ["MaleoSharedResults", "MaleoSharedClientResults", "MaleoSharedServiceResults", "MaleoSharedQueryResults"]