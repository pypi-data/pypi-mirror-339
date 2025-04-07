from __future__ import annotations
from fastapi import responses, status
from typing import Any
from pydantic import BaseModel, Field
from .response_class import BaseServiceRESTControllerResponseClass

class BaseServiceRESTControllerResults(BaseModel):
    success:bool = Field(..., description="REST Controller's success status")
    response_class:BaseServiceRESTControllerResponseClass = Field(BaseServiceRESTControllerResponseClass.JSON, description="REST Controller's response class")
    content:Any = Field(..., description="REST Controller's response content")
    status_code:int = Field(status.HTTP_200_OK, description="REST Controller's response status code")

    class Config:
        arbitrary_types_allowed=True

    def to_response(self) -> responses.Response:
        """Dynamically creates a response based on response_class."""
        response_cls = self.response_class.get_response_class()
        return response_cls(content=self.content, status_code=self.status_code)