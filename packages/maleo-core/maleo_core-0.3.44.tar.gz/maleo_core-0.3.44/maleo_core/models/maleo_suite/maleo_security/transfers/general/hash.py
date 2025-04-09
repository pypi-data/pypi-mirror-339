from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoSecurityHashGeneralTransfers:
    class Base(BaseModel):
        message:str = Field(..., description="Message to be hashed")

    class Hash(BaseModel):
        hash:str = Field(..., description="Hash value")