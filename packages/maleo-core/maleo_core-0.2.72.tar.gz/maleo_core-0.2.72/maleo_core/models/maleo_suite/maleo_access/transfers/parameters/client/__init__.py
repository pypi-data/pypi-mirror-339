# This file serves all MaleoAccess's Cient Parameters

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeClientParameters
from .gender import MaleoAccessGenderClientParameters
from .organization_role import MaleoAccessOrganizationRoleClientParameters
from .organization_type import MaleoAccessOrganizationTypeClientParameters
from .organization import MaleoAccessOrganizationClientParameters
from .system_role import MaleoAccessSystemRoleClientParameters
from .user_type import MaleoAccessUserTypeClientParameters

class MaleoAccessClientParameters:
    BloodType = MaleoAccessBloodTypeClientParameters
    Gender = MaleoAccessGenderClientParameters
    OrganizationRole = MaleoAccessOrganizationRoleClientParameters
    OrganizationType = MaleoAccessOrganizationTypeClientParameters
    Organization = MaleoAccessOrganizationClientParameters
    SystemRole = MaleoAccessSystemRoleClientParameters
    UserType = MaleoAccessUserTypeClientParameters

__all__ = [
    "MaleoAccessClientParameters",
    "MaleoAccessBloodTypeClientParameters",
    "MaleoAccessGenderClientParameters",
    "MaleoAccessOrganizationRoleClientParameters",
    "MaleoAccessOrganizationTypeClientParameters",
    "MaleoAccessOrganizationClientParameters",
    "MaleoAccessSystemRoleClientParameters",
    "MaleoAccessUserTypeClientParameters"
]