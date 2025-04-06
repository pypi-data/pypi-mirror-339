from .blood_type import MaleoAccessBloodTypeHTTPService
from .gender import MaleoAccessGenderHTTPService
from .organization_role import MaleoAccessOrganizationRoleHTTPService
from .organization_type import MaleoAccessOrganizationTypeHTTPService
from .organization import MaleoAccessOrganizationHTTPService
from .system_role import MaleoAccessSystemRoleHTTPService
from .user_type import MaleoAccessUserTypeHTTPService

class MaleoAccessHTTPServices:
    BloodType = MaleoAccessBloodTypeHTTPService
    Gender = MaleoAccessGenderHTTPService
    OrganizationRole = MaleoAccessOrganizationRoleHTTPService
    OrganizationType = MaleoAccessOrganizationTypeHTTPService
    Organization = MaleoAccessOrganizationHTTPService
    SystemRole = MaleoAccessSystemRoleHTTPService
    UserType = MaleoAccessUserTypeHTTPService