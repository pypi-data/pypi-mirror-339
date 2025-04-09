from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoSecurityKeyGeneralParameters:
    class GeneratePairOrPrivate(BaseModel):
        key_size:int = Field(2048, ge=1024, description="Key's size")

    class GeneratePublic(BaseModel):
        private_key:str = Field(..., description="Private key in str")