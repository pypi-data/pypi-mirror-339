# This file serves all MaleoAccess's Service Parameters

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeServiceParameters
from .gender import MaleoAccessGenderServiceParameters
from .organization_role import MaleoAccessOrganizationRoleServiceParameters
from .organization_type import MaleoAccessOrganizationTypeServiceParameters
from .organization import MaleoAccessOrganizationServiceParameters
from .system_role import MaleoAccessSystemRoleServiceParameters
from .user_type import MaleoAccessUserTypeServiceParameters
from .user import MaleoAccessUserServiceParameters

class MaleoAccessServiceParameters:
    BloodType = MaleoAccessBloodTypeServiceParameters
    Gender = MaleoAccessGenderServiceParameters
    OrganizationRole = MaleoAccessOrganizationRoleServiceParameters
    OrganizationType = MaleoAccessOrganizationTypeServiceParameters
    Organization = MaleoAccessOrganizationServiceParameters
    SystemRole = MaleoAccessSystemRoleServiceParameters
    UserType = MaleoAccessUserTypeServiceParameters
    User = MaleoAccessUserServiceParameters

__all__ = [
    "MaleoAccessServiceParameters",
    "MaleoAccessBloodTypeServiceParameters",
    "MaleoAccessGenderServiceParameters",
    "MaleoAccessOrganizationRoleServiceParameters",
    "MaleoAccessOrganizationTypeServiceParameters",
    "MaleoAccessOrganizationServiceParameters",
    "MaleoAccessSystemRoleServiceParameters",
    "MaleoAccessUserTypeServiceParameters",
    "MaleoAccessUserServiceParameters"
]