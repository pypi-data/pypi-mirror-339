from .manager import MaleoSecurityHTTPClientManager
from .controllers import MaleoSecurityHTTPControllers
from .services import MaleoSecurityHTTPServices

class MaleoSecurityHTTPClient:
    Manager = MaleoSecurityHTTPClientManager
    Controllers = MaleoSecurityHTTPControllers
    Services = MaleoSecurityHTTPServices