# This file serves all MaleoAccess Services Results

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeServiceResults
from .gender import MaleoAccessGenderServiceResults
from .organization_role import MaleoAccessOrganizationRoleServiceResults
from .organization_type import MaleoAccessOrganizationTypeServiceResults
from .organization import MaleoAccessOrganizationServiceResults
from .system_role import MaleoAccessSystemRoleServiceResults
from .user_organization_role import MaleoAccessUserOrganizationRoleServiceResults
from .user_organization import MaleoAccessUserOrganizationServiceResults
from .user_profile import MaleoAccessUserProfileServiceResults
from .user_system_role import MaleoAccessUserSystemRoleServiceResults
from .user_type import MaleoAccessUserTypeServiceResults
from .user import MaleoAccessUserServiceResults

class MaleoAccessServiceResults:
    BloodType = MaleoAccessBloodTypeServiceResults
    Gender = MaleoAccessGenderServiceResults
    OrganizationRole = MaleoAccessOrganizationRoleServiceResults
    OrganizationType = MaleoAccessOrganizationTypeServiceResults
    Organization = MaleoAccessOrganizationServiceResults
    SystemRole = MaleoAccessSystemRoleServiceResults
    UserOrganizationRole = MaleoAccessUserOrganizationRoleServiceResults
    UserOrganization = MaleoAccessUserOrganizationServiceResults
    UserProfile = MaleoAccessUserProfileServiceResults
    UserSystemRole = MaleoAccessUserSystemRoleServiceResults
    UserType = MaleoAccessUserTypeServiceResults
    User = MaleoAccessUserServiceResults

__all__ = [
    "MaleoAccessServiceResults",
    "MaleoAccessBloodTypeServiceResults",
    "MaleoAccessGenderServiceResults",
    "MaleoAccessOrganizationRoleServiceResults",
    "MaleoAccessOrganizationTypeServiceResults",
    "MaleoAccessOrganizationServiceResults",
    "MaleoAccessSystemRoleServiceResults",
    "MaleoAccessUserOrganizationRoleServiceResults",
    "MaleoAccessUserOrganizationServiceResults",
    "MaleoAccessUserProfileServiceResults",
    "MaleoAccessUserSystemRoleServiceResults",
    "MaleoAccessUserTypeServiceResults",
    "MaleoAccessUserServiceResults"
]