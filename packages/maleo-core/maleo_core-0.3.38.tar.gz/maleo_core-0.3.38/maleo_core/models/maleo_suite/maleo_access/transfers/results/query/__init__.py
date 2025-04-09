# This file serves all MaleoAccess's query results

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeQueryResults
from .gender import MaleoAccessGenderQueryResults
from .organization_role import MaleoAccessOrganizationRoleQueryResults
from .organization_type import MaleoAccessOrganizationTypeQueryResults
from .organization import MaleoAccessOrganizationQueryResults
from .system_role import MaleoAccessSystemRoleQueryResults
from .user_organization_role import MaleoAccessUserOrganizationRoleQueryResults
from .user_profile import MaleoAccessUserProfileQueryResults
from .user_system_role import MaleoAccessUserSystemRoleQueryResults
from .user_type import MaleoAccessUserTypeQueryResults
from .user import MaleoAccessUserQueryResults

class MaleoAccessQueryResults:
    BloodType = MaleoAccessBloodTypeQueryResults
    Gender = MaleoAccessGenderQueryResults
    OrganizationRole = MaleoAccessOrganizationRoleQueryResults
    OrganizationType = MaleoAccessOrganizationTypeQueryResults
    Organization = MaleoAccessOrganizationQueryResults
    SystemRole = MaleoAccessSystemRoleQueryResults
    UserOrganizationRole = MaleoAccessUserOrganizationRoleQueryResults
    UserProfile = MaleoAccessUserProfileQueryResults
    UserSystemRole = MaleoAccessUserSystemRoleQueryResults
    UserType = MaleoAccessUserTypeQueryResults
    User = MaleoAccessUserQueryResults

__all__ = [
    "MaleoAccessQueryResults",
    "MaleoAccessBloodTypeQueryResults",
    "MaleoAccessGenderQueryResults",
    "MaleoAccessOrganizationRoleQueryResults",
    "MaleoAccessOrganizationTypeQueryResults",
    "MaleoAccessOrganizationQueryResults",
    "MaleoAccessSystemRoleQueryResults",
    "MaleoAccessUserOrganizationRoleQueryResults",
    "MaleoAccessUserProfileQueryResults",
    "MaleoAccessUserSystemRoleQueryResults",
    "MaleoAccessUserTypeQueryResults",
    "MaleoAccessUserQueryResults"
]