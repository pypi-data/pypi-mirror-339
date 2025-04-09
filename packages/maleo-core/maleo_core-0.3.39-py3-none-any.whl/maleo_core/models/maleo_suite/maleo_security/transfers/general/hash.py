from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoSecurityHashGeneralTransfers:
    class Base(BaseModel):
        hash:str = Field(..., description="Hash value")