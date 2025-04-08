# This file serves all MaleoAccess's General Parameters

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeGeneralParameters
from .gender import MaleoAccessGenderGeneralParameters
from .organization_role import MaleoAccessOrganizationRoleGeneralParameters
from .organization_type import MaleoAccessOrganizationTypeGeneralParameters
from .organization import MaleoAccessOrganizationGeneralParameters
from .system_role import MaleoAccessSystemRoleGeneralParameters
from .user_organization_role import MaleoAccessUserOrganizationRoleGeneralParameters
from .user_organization import MaleoAccessUserOrganizationGeneralParameters
from .user_profile import MaleoAccessUserProfileGeneralParameters
from .user_system_role import MaleoAccessUserSystemRoleGeneralParameters
from .user_type import MaleoAccessUserTypeGeneralParameters
from .user import MaleoAccessUserGeneralParameters

class MaleoAcccesGeneralParameters:
    BloodType = MaleoAccessBloodTypeGeneralParameters
    Gender = MaleoAccessGenderGeneralParameters
    OrganizationRole = MaleoAccessOrganizationRoleGeneralParameters
    OrganizationType = MaleoAccessOrganizationTypeGeneralParameters
    Organization = MaleoAccessOrganizationGeneralParameters
    SystemRole = MaleoAccessSystemRoleGeneralParameters
    UserOrganizationRole = MaleoAccessUserOrganizationRoleGeneralParameters
    UserOrganization = MaleoAccessUserOrganizationGeneralParameters
    UserProfile = MaleoAccessUserProfileGeneralParameters
    UserSystemRole = MaleoAccessUserSystemRoleGeneralParameters
    UserType = MaleoAccessUserTypeGeneralParameters
    User = MaleoAccessUserGeneralParameters

__all__ = [
    "MaleoAcccesGeneralParameters",
    "MaleoAccessBloodTypeGeneralParameters",
    "MaleoAccessGenderGeneralParameters",
    "MaleoAccessOrganizationRoleGeneralParameters",
    "MaleoAccessOrganizationTypeGeneralParameters",
    "MaleoAccessOrganizationGeneralParameters",
    "MaleoAccessSystemRoleGeneralParameters",
    "MaleoAccessUserOrganizationRoleGeneralParameters",
    "MaleoAccessUserOrganizationGeneralParameters",
    "MaleoAccessUserProfileGeneralParameters",
    "MaleoAccessUserSystemRoleGeneralParameters",
    "MaleoAccessUserTypeGeneralParameters",
    "MaleoAccessUserGeneralParameters"
]