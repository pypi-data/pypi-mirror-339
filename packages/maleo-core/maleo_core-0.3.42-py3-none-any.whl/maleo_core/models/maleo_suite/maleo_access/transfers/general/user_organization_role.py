from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoAccessUserOrganizationRoleGeneralTransfers:
    class Base(BaseModel):
        user_organization_id:int = Field(..., ge=1, description="User organization's id")
        organization_role_id:int = Field(..., ge=1, description="Organization role's id")