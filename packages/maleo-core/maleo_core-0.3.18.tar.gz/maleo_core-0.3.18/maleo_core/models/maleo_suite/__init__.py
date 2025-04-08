# This file serves all MaleoSuite's models

from .maleo_shared import MaleoSharedModels
from .maleo_access import MaleoAccessModels

class MaleoSuiteModels:
    MaleoShared = MaleoSharedModels
    MaleoAccess = MaleoAccessModels

__all__ = [
    "MaleoSuiteModels",
    "MaleoSharedModels",
    "MaleoAccessModels"
]