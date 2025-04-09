# This file serves all MaleoSuite's models

from .maleo_shared import MaleoSharedModels
from .maleo_security import MaleoSecurityModels
from .maleo_access import MaleoAccessModels

class MaleoSuiteModels:
    MaleoShared = MaleoSharedModels
    MaleoSecurity = MaleoSecurityModels
    MaleoAccess = MaleoAccessModels

__all__ = [
    "MaleoSuiteModels",
    "MaleoSharedModels",
    "MaleoSecurityModels",
    "MaleoAccessModels"
]