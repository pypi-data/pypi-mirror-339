from .secret import MaleoSecuritySecretHTTPService
from .key import MaleoSecurityKeyHTTPService
from .encryption import MaleoSecurityEncryptionHTTPService

class MaleoSecurityHTTPServices:
    Secret = MaleoSecuritySecretHTTPService
    Key = MaleoSecurityKeyHTTPService
    Encryption = MaleoSecurityEncryptionHTTPService