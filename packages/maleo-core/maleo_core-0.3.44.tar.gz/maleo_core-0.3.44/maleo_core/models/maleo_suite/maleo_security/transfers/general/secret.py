from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional
from maleo_core.models.base.transfers.results.general import BaseGeneralResults

class MaleoSecuritySecretGeneralTransfers:
    class Base(BaseModel):
        name:str = Field(..., description="Secret's name")

    class GetParameters(Base):
        version:str = Field("latest", description="Secret's version. Default to 'latest'")

    class CreateParameters(Base):
        data:str = Field(..., description="Secret's data")

    class Results(Base):
        data:str = Field(..., description="Secret's data")

    Fail = BaseGeneralResults.Fail

    class SingleData(BaseGeneralResults.SingleData):
        data:Optional[MaleoSecuritySecretGeneralTransfers.Results]