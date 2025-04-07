from .blood_type import MaleoAccessBloodTypeHTTPController
from .gender import MaleoAccessGenderHTTPController
from .organization_role import MaleoAccessOrganizationRoleHTTPController
from .organization_type import MaleoAccessOrganizationTypeHTTPController
from .organization import MaleoAccessOrganizationHTTPController
from .system_role import MaleoAccessSystemRoleHTTPController
from .user_profile import MaleoAccessUserProfileHTTPController
from .user_type import MaleoAccessUserTypeHTTPController
from .user import MaleoAccessUserHTTPController

class MaleoAccessHTTPControllers:
    BloodType = MaleoAccessBloodTypeHTTPController
    Gender = MaleoAccessGenderHTTPController
    OrganizationRole = MaleoAccessOrganizationRoleHTTPController
    OrganizationType = MaleoAccessOrganizationTypeHTTPController
    Organization = MaleoAccessOrganizationHTTPController
    SystemRole = MaleoAccessSystemRoleHTTPController
    UserProfile = MaleoAccessUserProfileHTTPController
    UserType = MaleoAccessUserTypeHTTPController
    User = MaleoAccessUserHTTPController