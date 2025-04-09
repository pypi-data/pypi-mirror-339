from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoAccessUserSystemRoleGeneralTransfers:
    class Base(BaseModel):
        user_id:int = Field(..., ge=1, description="User's id")
        system_role_id:int = Field(..., ge=1, description="System role's id")