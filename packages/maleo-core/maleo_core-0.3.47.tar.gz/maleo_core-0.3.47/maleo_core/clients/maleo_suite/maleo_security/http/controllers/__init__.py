from .secret import MaleoSecuritySecretHTTPController
from .key import MaleoSecurityKeyHTTPController
from .encryption import MaleoSecurityEncryptionHTTPController

class MaleoSecurityHTTPControllers:
    Secret = MaleoSecuritySecretHTTPController
    Key = MaleoSecurityKeyHTTPController
    Encryption = MaleoSecurityEncryptionHTTPController