from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoAccessUserOrganizationGeneralTransfers:
    class Base(BaseModel):
        user_id:int = Field(..., ge=1, description="User's id")
        organization_id:int = Field(..., ge=1, description="Organization's id")