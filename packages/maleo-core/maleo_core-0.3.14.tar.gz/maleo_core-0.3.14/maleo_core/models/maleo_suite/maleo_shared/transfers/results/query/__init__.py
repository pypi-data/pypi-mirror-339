# This file serves all MaleoShared's query results

from __future__ import annotations
from .service import MaleoSharedServiceQueryResults

class MaleoSharedQueryResults:
    Service = MaleoSharedServiceQueryResults

__all__ = ["MaleoSharedQueryResults", "MaleoSharedServiceQueryResults"]