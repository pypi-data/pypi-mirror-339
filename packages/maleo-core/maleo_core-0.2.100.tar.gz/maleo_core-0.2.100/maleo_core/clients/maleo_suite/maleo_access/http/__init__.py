from .manager import MaleoAccessHTTPClientManager
from .controllers import MaleoAccessHTTPControllers
from .services import MaleoAccessHTTPServices

class MaleoAccessHTTPClient:
    Manager = MaleoAccessHTTPClientManager
    Controllers = MaleoAccessHTTPControllers
    Services = MaleoAccessHTTPServices