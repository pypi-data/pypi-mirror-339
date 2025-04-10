from .bcrypt import MaleoSecurityBcryptHashHTTPController
from .hmac import MaleoSecurityHMACHashHTTPController
from .sha256 import MaleoSecuritySHA256HashHTTPController

class MaleoSecurityHashHTTPController:
    Bcrypt = MaleoSecurityBcryptHashHTTPController
    HMAC = MaleoSecurityHMACHashHTTPController
    SHA256 = MaleoSecuritySHA256HashHTTPController