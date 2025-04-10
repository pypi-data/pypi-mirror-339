from .bcrypt import MaleoSecurityBcryptHashHTTPService
from .hmac import MaleoSecurityHMACHashHTTPService
from .sha256 import MaleoSecuritySHA256HashHTTPService

class MaleoSecurityHashHTTPService:
    Bcrypt = MaleoSecurityBcryptHashHTTPService
    HMAC = MaleoSecurityHMACHashHTTPService
    SHA256 = MaleoSecuritySHA256HashHTTPService