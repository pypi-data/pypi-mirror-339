from .manager import MaleoSharedHTTPClientManager
from .controllers import MaleoSharedHTTPControllers
from .services import MaleoSharedHTTPServices

class MaleoSharedHTTPClient:
    Manager = MaleoSharedHTTPClientManager
    Controllers = MaleoSharedHTTPControllers
    Services = MaleoSharedHTTPServices