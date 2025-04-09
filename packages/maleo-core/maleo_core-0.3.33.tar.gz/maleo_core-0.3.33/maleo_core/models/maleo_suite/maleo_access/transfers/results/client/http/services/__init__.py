# This file serves all MaleoAccess's HTTP Client Services Results

from __future__ import annotations
from .blood_type import MaleoAccessHTTPClientBloodTypeServiceResults
from .gender import MaleoAccessHTTPClientGenderServiceResults
from .organization_role import MaleoAccessHTTPClientOrganizationRoleServiceResults
from .organization_type import MaleoAccessHTTPClientOrganizationTypeServiceResults
from .organization import MaleoAccessHTTPClientOrganizationServiceResults
from .system_role import MaleoAccessHTTPClientSystemRoleServiceResults
from .user_organization_role import MaleoAccessHTTPClientUserOrganizationRoleServiceResults
from .user_organization import MaleoAccessHTTPClientUserOrganizationServiceResults
from .user_profile import MaleoAccessHTTPClientUserProfileServiceResults
from .user_system_role import MaleoAccessHTTPClientUserSystemRoleServiceResults
from .user_type import MaleoAccessHTTPClientUserTypeServiceResults
from .user import MaleoAccessHTTPClientUserServiceResults

class MaleoAccessHTTPClientServicesResults:
    BloodType = MaleoAccessHTTPClientBloodTypeServiceResults
    Gender = MaleoAccessHTTPClientGenderServiceResults
    OrganizationRole = MaleoAccessHTTPClientOrganizationRoleServiceResults
    OrganizationType = MaleoAccessHTTPClientOrganizationTypeServiceResults
    Organization = MaleoAccessHTTPClientOrganizationServiceResults
    SystemRole = MaleoAccessHTTPClientSystemRoleServiceResults
    UserOrganizationRole = MaleoAccessHTTPClientUserOrganizationRoleServiceResults
    UserOrganization = MaleoAccessHTTPClientUserOrganizationServiceResults
    UserProfile = MaleoAccessHTTPClientUserProfileServiceResults
    UserSystemRole = MaleoAccessHTTPClientUserSystemRoleServiceResults
    UserType = MaleoAccessHTTPClientUserTypeServiceResults
    User = MaleoAccessHTTPClientUserServiceResults

__all__ = [
    "MaleoAccessHTTPClientServicesResults",
    "MaleoAccessHTTPClientBloodTypeServiceResults",
    "MaleoAccessHTTPClientGenderServiceResults",
    "MaleoAccessHTTPClientOrganizationRoleServiceResults",
    "MaleoAccessHTTPClientOrganizationTypeServiceResults",
    "MaleoAccessHTTPClientOrganizationServiceResults",
    "MaleoAccessHTTPClientSystemRoleServiceResults",
    "MaleoAccessHTTPClientUserOrganizationRoleServiceResults",
    "MaleoAccessHTTPClientUserOrganizationServiceResults",
    "MaleoAccessHTTPClientUserProfileServiceResults",
    "MaleoAccessHTTPClientUserSystemRoleServiceResults",
    "MaleoAccessHTTPClientUserTypeServiceResults",
    "MaleoAccessHTTPClientUserServiceResults"
]