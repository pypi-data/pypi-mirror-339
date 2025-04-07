from __future__ import annotations
from httpx import Response
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Any

class BaseHTTPClientControllerResults(BaseModel):
    response:Response = Field(..., description="HTTP Client's response")
    status_code:int = Field(..., description="HTTP Client's response status code")
    content:Any = Field(..., description="HTTP Client's response content")
    success:bool = Field(..., description="HTTP Client's success status")

    class Config:
        arbitrary_types_allowed=True

    @model_validator(mode="before")
    @classmethod
    def process_response(cls, values:dict) -> dict:
        """Process the response to set status_code, content, and success."""
        response:Response = values.get("response")

        if response:
            values["status_code"] = response.status_code
            values["success"] = response.is_success

            #* Determine content type and parse accordingly
            content_type = response.headers.get("content-type", "").lower()

            if "application/json" in content_type:
                values["content"] = response.json()
            elif "text/" in content_type or "application/xml" in content_type:
                values["content"] = response.text
            else:
                values["content"] = response.content  #* Raw bytes for unknown types

        return values