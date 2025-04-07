from __future__ import annotations
from enum import StrEnum
from fastapi import responses

class BaseServiceRESTControllerResponseClass(StrEnum):
    NONE = "none"
    HTML = "html"
    TEXT = "text"
    JSON = "json"
    REDIRECT = "redirect"
    STREAMING = "streaming"
    FILE = "file"

    def get_response_class(self) -> type[responses.Response]:
        """Returns the corresponding FastAPI Response class."""
        return {
            BaseServiceRESTControllerResponseClass.NONE: responses.Response,
            BaseServiceRESTControllerResponseClass.HTML: responses.HTMLResponse,
            BaseServiceRESTControllerResponseClass.TEXT: responses.PlainTextResponse,
            BaseServiceRESTControllerResponseClass.JSON: responses.JSONResponse,
            BaseServiceRESTControllerResponseClass.REDIRECT: responses.RedirectResponse,
            BaseServiceRESTControllerResponseClass.STREAMING: responses.StreamingResponse,
            BaseServiceRESTControllerResponseClass.FILE: responses.FileResponse,
        }.get(self, responses.Response)