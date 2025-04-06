from .blood_type import MaleoAccessBloodTypeHTTPController
from .gender import MaleoAccessGenderHTTPController
from .organization_role import MaleoAccessOrganizationRoleHTTPController
from .organization_type import MaleoAccessOrganizationTypeHTTPController
from .organization import MaleoAccessOrganizationHTTPController
from .system_role import MaleoAccessSystemRoleHTTPController
from .user_type import MaleoAccessUserTypeHTTPController

class MaleoAccessHTTPControllers:
    BloodType = MaleoAccessBloodTypeHTTPController
    Gender = MaleoAccessGenderHTTPController
    OrganizationRole = MaleoAccessOrganizationRoleHTTPController
    OrganizationType = MaleoAccessOrganizationTypeHTTPController
    Organization = MaleoAccessOrganizationHTTPController
    SystemRole = MaleoAccessSystemRoleHTTPController
    UserType = MaleoAccessUserTypeHTTPController