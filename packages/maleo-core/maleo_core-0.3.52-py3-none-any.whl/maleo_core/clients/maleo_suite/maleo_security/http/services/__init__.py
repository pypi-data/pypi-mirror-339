from .secret import MaleoSecuritySecretHTTPService
from .key import MaleoSecurityKeyHTTPService
from .encryption import MaleoSecurityEncryptionHTTPService
from .hash import MaleoSecurityHashHTTPService

class MaleoSecurityHTTPServices:
    Secret = MaleoSecuritySecretHTTPService
    Key = MaleoSecurityKeyHTTPService
    Encryption = MaleoSecurityEncryptionHTTPService
    Hash = MaleoSecurityHashHTTPService