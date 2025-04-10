from .aes import MaleoSecurityAESEncryptionHTTPController
from .rsa import MaleoSecurityRSAEncryptionHTTPController

class MaleoSecurityEncryptionHTTPController:
    AES = MaleoSecurityAESEncryptionHTTPController
    RSA = MaleoSecurityRSAEncryptionHTTPController