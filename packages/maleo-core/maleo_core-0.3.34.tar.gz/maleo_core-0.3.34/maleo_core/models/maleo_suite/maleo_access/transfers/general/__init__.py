# This file serves all MaleoAccess's General Transfers

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeGeneralTransfers
from .gender import MaleoAccessGenderGeneralTransfers
from .organization_role import MaleoAccessOrganizationRoleGeneralTransfers
from .organization_type import MaleoAccessOrganizationTypeGeneralTransfers
from .organization import MaleoAccessOrganizationGeneralTransfers
from .system_role import MaleoAccessSystemRoleGeneralTransfers
from .user_organization import MaleoAccessUserOrganizationGeneralTransfers
from .user_organization_role import MaleoAccessUserOrganizationRoleGeneralTransfers
from .user_profile import MaleoAccessUserProfileGeneralTransfers
from .user_system_role import MaleoAccessUserSystemRoleGeneralTransfers
from .user_type import MaleoAccessUserTypeGeneralTransfers
from .user import MaleoAccessUserGeneralTransfers

class MaleoAccessGeneralTransfers:
    BloodType = MaleoAccessBloodTypeGeneralTransfers
    Gender = MaleoAccessGenderGeneralTransfers
    OrganizationRole = MaleoAccessOrganizationRoleGeneralTransfers
    OrganizationType = MaleoAccessOrganizationTypeGeneralTransfers
    Organization = MaleoAccessOrganizationGeneralTransfers
    SystemRole = MaleoAccessSystemRoleGeneralTransfers
    UserOrganization = MaleoAccessUserOrganizationGeneralTransfers
    UserOrganizationRole = MaleoAccessUserOrganizationRoleGeneralTransfers
    UserProfile = MaleoAccessUserProfileGeneralTransfers
    UserSystemRole = MaleoAccessUserSystemRoleGeneralTransfers
    UserType = MaleoAccessUserTypeGeneralTransfers
    User = MaleoAccessUserGeneralTransfers

__all__ = [
    "MaleoAccessGeneralTransfers",
    "MaleoAccessBloodTypeGeneralTransfers",
    "MaleoAccessGenderGeneralTransfers",
    "MaleoAccessOrganizationRoleGeneralTransfers",
    "MaleoAccessOrganizationTypeGeneralTransfers",
    "MaleoAccessOrganizationGeneralTransfers",
    "MaleoAccessSystemRoleGeneralTransfers",
    "MaleoAccessUserOrganizationGeneralTransfers",
    "MaleoAccessUserOrganizationRoleGeneralTransfers",
    "MaleoAccessUserProfileGeneralTransfers",
    "MaleoAccessUserSystemRoleGeneralTransfers",
    "MaleoAccessUserTypeGeneralTransfers",
    "MaleoAccessUserGeneralTransfers"
]