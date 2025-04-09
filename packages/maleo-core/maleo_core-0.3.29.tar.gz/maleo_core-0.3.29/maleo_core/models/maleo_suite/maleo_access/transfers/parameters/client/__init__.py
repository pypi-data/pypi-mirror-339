# This file serves all MaleoAccess's Cient Parameters

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeClientParameters
from .gender import MaleoAccessGenderClientParameters
from .organization_role import MaleoAccessOrganizationRoleClientParameters
from .organization_type import MaleoAccessOrganizationTypeClientParameters
from .organization import MaleoAccessOrganizationClientParameters
from .system_role import MaleoAccessSystemRoleClientParameters
from .user_organization_role import MaleoAccessUserOrganizationRoleClientParameters
from .user_organization import MaleoAccessUserOrganizationClientParameters
from .user_profile import MaleoAccessUserProfileClientParameters
from .user_system_role import MaleoAccessUserSystemRoleClientParameters
from .user_type import MaleoAccessUserTypeClientParameters
from .user import MaleoAccessUserClientParameters

class MaleoAccessClientParameters:
    BloodType = MaleoAccessBloodTypeClientParameters
    Gender = MaleoAccessGenderClientParameters
    OrganizationRole = MaleoAccessOrganizationRoleClientParameters
    OrganizationType = MaleoAccessOrganizationTypeClientParameters
    Organization = MaleoAccessOrganizationClientParameters
    SystemRole = MaleoAccessSystemRoleClientParameters
    UserOrganizationRole = MaleoAccessUserOrganizationRoleClientParameters
    UserOrganization = MaleoAccessUserOrganizationClientParameters
    UserProfile = MaleoAccessUserProfileClientParameters
    UserSystemRole = MaleoAccessUserSystemRoleClientParameters
    UserType = MaleoAccessUserTypeClientParameters
    User = MaleoAccessUserClientParameters

__all__ = [
    "MaleoAccessClientParameters",
    "MaleoAccessBloodTypeClientParameters",
    "MaleoAccessGenderClientParameters",
    "MaleoAccessOrganizationRoleClientParameters",
    "MaleoAccessOrganizationTypeClientParameters",
    "MaleoAccessOrganizationClientParameters",
    "MaleoAccessSystemRoleClientParameters",
    "MaleoAccessUserOrganizationRoleClientParameters",
    "MaleoAccessUserOrganizationClientParameters",
    "MaleoAccessUserProfileClientParameters",
    "MaleoAccessUserSystemRoleClientParameters",
    "MaleoAccessUserTypeClientParameters",
    "MaleoAccessUserClientParameters"
]