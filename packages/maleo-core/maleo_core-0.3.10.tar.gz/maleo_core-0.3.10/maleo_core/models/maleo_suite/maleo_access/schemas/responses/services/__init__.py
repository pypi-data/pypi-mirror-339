# This file serves all MaleoAccess's services responses schemas

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeServiceResponsesSchemas
from .gender import MaleoAccessGenderServiceResponsesSchemas
from .organization_role import MaleoAccessOrganizationRoleServiceResponsesSchemas
from .organization_type import MaleoAccessOrganizationTypeServiceResponsesSchemas
from .organization import MaleoAccessOrganizationServiceResponsesSchemas
from .system_role import MaleoAccessSystemRoleServiceResponsesSchemas
from .user_type import MaleoAccessUserTypeServiceResponsesSchemas

class MaleoAccessServicesResponsesSchemas:
    BloodType = MaleoAccessBloodTypeServiceResponsesSchemas
    Gender = MaleoAccessGenderServiceResponsesSchemas
    OrganizationRole = MaleoAccessOrganizationRoleServiceResponsesSchemas
    OrganizationType = MaleoAccessOrganizationTypeServiceResponsesSchemas
    Organization = MaleoAccessOrganizationServiceResponsesSchemas
    SystemRole = MaleoAccessSystemRoleServiceResponsesSchemas
    UserType = MaleoAccessUserTypeServiceResponsesSchemas

__all__ = [
    "MaleoAccessServicesResponsesSchemas",
    "MaleoAccessBloodTypeServiceResponsesSchemas",
    "MaleoAccessGenderServiceResponsesSchemas",
    "MaleoAccessOrganizationRoleServiceResponsesSchemas",
    "MaleoAccessOrganizationTypeServiceResponsesSchemas",
    "MaleoAccessOrganizationServiceResponsesSchemas",
    "MaleoAccessSystemRoleServiceResponsesSchemas",
    "MaleoAccessUserTypeServiceResponsesSchemas"
]