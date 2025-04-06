# This file serves all MaleoAccess's General Transfers

from __future__ import annotations
from .blood_type import MaleoAccessBloodTypeGeneralTransfers
from .gender import MaleoAccessGenderGeneralTransfers
from .organization_role import MaleoAccessOrganizationRoleGeneralTransfers
from .organization_type import MaleoAccessOrganizationTypeGeneralTransfers
from .organization import MaleoAccessOrganizationGeneralTransfers
from .system_role import MaleoAccessSystemRoleGeneralTransfers
from .user_type import MaleoAccessUserTypeGeneralTransfers

class MaleoAccessGeneralTransfers:
    BloodType = MaleoAccessBloodTypeGeneralTransfers
    Gender = MaleoAccessGenderGeneralTransfers
    OrganizationRole = MaleoAccessOrganizationRoleGeneralTransfers
    OrganizationType = MaleoAccessOrganizationTypeGeneralTransfers
    Organization = MaleoAccessOrganizationGeneralTransfers
    SystemRole = MaleoAccessSystemRoleGeneralTransfers
    UserType = MaleoAccessUserTypeGeneralTransfers

__all__ = [
    "MaleoAccessGeneralTransfers",
    "MaleoAccessBloodTypeGeneralTransfers",
    "MaleoAccessGenderGeneralTransfers",
    "MaleoAccessOrganizationRoleGeneralTransfers",
    "MaleoAccessOrganizationTypeGeneralTransfers",
    "MaleoAccessOrganizationGeneralTransfers",
    "MaleoAccessSystemRoleGeneralTransfers",
    "MaleoAccessUserTypeGeneralTransfers"
]