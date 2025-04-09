import os
from typing import Optional
from maleo_core.clients.general.http import HTTPClientManager

class MaleoSecurityHTTPClientManager(HTTPClientManager):
    _base_url:Optional[str] = None

    @classmethod
    def initialize(cls, base_url:Optional[str] = None) -> None:
        """Initialize the maleo-security client if not already initialized."""
        super().initialize()  #* Initialize HTTP Client Manager

        cls._base_url = base_url or os.getenv("MALEO_SECURITY_BASE_URL")
        if cls._base_url is None:
            raise ValueError("MALEO_SECURITY_BASE_URL environment variable must be set if no base_url is provided")
        cls._base_url += "/api"

    @classmethod
    async def dispose(cls) -> None:
        """Dispose of the maleo-security client and release any resources."""
        await super().dispose()  #* Dispose HTTP Client Manager

        if cls._base_url is not None:
            cls._base_url = None