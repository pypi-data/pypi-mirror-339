from .aes import MaleoSecurityAESEncryptionHTTPService
from .rsa import MaleoSecurityRSAEncryptionHTTPService

class MaleoSecurityEncryptionHTTPService:
    AES = MaleoSecurityAESEncryptionHTTPService
    RSA = MaleoSecurityRSAEncryptionHTTPService