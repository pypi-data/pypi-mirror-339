# This file serves all MaleoAccess's services responses schemas

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeServiceResponsesSchemas
from .gender import MaleoAccessGenderServiceResponsesSchemas
from .organization_role import MaleoAccessOrganizationRoleServiceResponsesSchemas
from .organization_type import MaleoAccessOrganizationTypeServiceResponsesSchemas
from .organization import MaleoAccessOrganizationServiceResponsesSchemas
from .system_role import MaleoAccessSystemRoleServiceResponsesSchemas
from .user_organization_role import MaleoAccessUserOrganizationRoleServiceResponsesSchemas
from .user_organization import MaleoAccessUserOrganizationServiceResponsesSchemas
from .user_profile import MaleoAccessUserProfileServiceResponsesSchemas
from .user_system_role import MaleoAccessUserSystemRoleServiceResponsesSchemas
from .user_type import MaleoAccessUserTypeServiceResponsesSchemas
from .user import MaleoAccessUserServiceResponsesSchemas

class MaleoAccessServicesResponsesSchemas:
    BloodType = MaleoAccessBloodTypeServiceResponsesSchemas
    Gender = MaleoAccessGenderServiceResponsesSchemas
    OrganizationRole = MaleoAccessOrganizationRoleServiceResponsesSchemas
    OrganizationType = MaleoAccessOrganizationTypeServiceResponsesSchemas
    Organization = MaleoAccessOrganizationServiceResponsesSchemas
    SystemRole = MaleoAccessSystemRoleServiceResponsesSchemas
    UserOrganizationRole = MaleoAccessUserOrganizationRoleServiceResponsesSchemas
    UserOrganization = MaleoAccessUserOrganizationServiceResponsesSchemas
    UserProfile = MaleoAccessUserProfileServiceResponsesSchemas
    UserSystemRole = MaleoAccessUserSystemRoleServiceResponsesSchemas
    UserType = MaleoAccessUserTypeServiceResponsesSchemas
    User = MaleoAccessUserServiceResponsesSchemas

__all__ = [
    "MaleoAccessServicesResponsesSchemas",
    "MaleoAccessBloodTypeServiceResponsesSchemas",
    "MaleoAccessGenderServiceResponsesSchemas",
    "MaleoAccessOrganizationRoleServiceResponsesSchemas",
    "MaleoAccessOrganizationTypeServiceResponsesSchemas",
    "MaleoAccessOrganizationServiceResponsesSchemas",
    "MaleoAccessSystemRoleServiceResponsesSchemas",
    "MaleoAccessUserOrganizationRoleServiceResponsesSchemas",
    "MaleoAccessUserOrganizationServiceResponsesSchemas",
    "MaleoAccessUserProfileServiceResponsesSchemas",
    "MaleoAccessUserSystemRoleServiceResponsesSchemas"
    "MaleoAccessUserTypeServiceResponsesSchemas",
    "MaleoAccessUserServiceResponsesSchemas"
]