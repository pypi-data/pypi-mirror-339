# This file serves all MaleoAccess's Service Parameters

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeServiceParameters
from .gender import MaleoAccessGenderServiceParameters
from .organization_role import MaleoAccessOrganizationRoleServiceParameters
from .organization_type import MaleoAccessOrganizationTypeServiceParameters
from .organization import MaleoAccessOrganizationServiceParameters
from .system_role import MaleoAccessSystemRoleServiceParameters
from .user_organization_role import MaleoAccessUserOrganizationRoleServiceParameters
from .user_organization import MaleoAccessUserOrganizationServiceParameters
from .user_profile import MaleoAccessUserProfileServiceParameters
from .user_system_role import MaleoAccessUserSystemRoleServiceParameters
from .user_type import MaleoAccessUserTypeServiceParameters
from .user import MaleoAccessUserServiceParameters

class MaleoAccessServiceParameters:
    BloodType = MaleoAccessBloodTypeServiceParameters
    Gender = MaleoAccessGenderServiceParameters
    OrganizationRole = MaleoAccessOrganizationRoleServiceParameters
    OrganizationType = MaleoAccessOrganizationTypeServiceParameters
    Organization = MaleoAccessOrganizationServiceParameters
    SystemRole = MaleoAccessSystemRoleServiceParameters
    UserOrganizationRole = MaleoAccessUserOrganizationRoleServiceParameters
    UserOrganization = MaleoAccessUserOrganizationServiceParameters
    UserProfile = MaleoAccessUserProfileServiceParameters
    UserSystemRole = MaleoAccessUserSystemRoleServiceParameters
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
    "MaleoAccessUserOrganizationRoleServiceParameters",
    "MaleoAccessUserOrganizationServiceParameters",
    "MaleoAccessUserProfileServiceParameters",
    "MaleoAccessUserSystemRoleServiceParameters",
    "MaleoAccessUserTypeServiceParameters",
    "MaleoAccessUserServiceParameters"
]