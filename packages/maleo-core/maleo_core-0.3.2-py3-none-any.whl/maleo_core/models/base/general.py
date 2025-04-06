from __future__ import annotations
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pydantic import BaseModel, Field, model_validator
from typing import Dict, List, Literal, Optional, Union
from uuid import UUID
from maleo_core.utils.constants import REFRESH_TOKEN_DURATION_DAYS, ACCESS_TOKEN_DURATION_MINUTES

class BaseGeneralModels:
    class AllowedMethods(StrEnum):
        OPTIONS = "OPTIONS"
        GET = "GET"
        POST = "POST"
        PATCH = "PATCH"
        PUT = "PUT"
        DELETE = "DELETE"
        ALL = "*"

    AllowedRoles = Union[List[int], Literal["*"]]
    RoutesPermissions = Dict[str, Dict[AllowedMethods, AllowedRoles]]

    class StatusType(StrEnum):
        DELETED = "deleted"
        INACTIVE = "inactive"
        ACTIVE = "active"

    class UserType(StrEnum):
        REGULAR = "regular"
        PROXY = "proxy"

    class SimplePagination(BaseModel):
        page:int = Field(1, ge=1, description="Page number, must be >= 1.")
        limit:int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.")

    class ExtendedPagination(SimplePagination):
        data_count:int = Field(..., description="Fetched data count")
        total_data:int = Field(..., description="Total data count")
        total_pages:int = Field(..., description="Total pages count")

    class SortOrder(StrEnum):
        ASC = "asc"
        DESC = "desc"

    class SortColumn(BaseModel):
        name:str = Field(..., description="Column name.")
        order:BaseGeneralModels.SortOrder = Field(..., description="Sort order.")

    class DateFilter(BaseModel):
        name:str = Field(..., description="Column name.")
        from_date:Optional[datetime] = Field(None, description="From date.")
        to_date:Optional[datetime] = Field(None, description="To date.")

    class Token(BaseModel):
        id:int
        uuid:UUID
        role_id:int
        scope:Literal["refresh", "access"]
        iat:datetime = datetime.now(timezone.utc)
        exp:datetime

        @model_validator(mode="before")
        def set_iat_and_exp(cls, values:dict):
            iat = values.get("iat", None)
            exp = values.get("iat", None)
            if not iat and not exp:
                iat = datetime.now(timezone.utc)
                values["iat"] = iat
                if values["scope"] == "refresh":
                    values["exp"] = iat + timedelta(days=REFRESH_TOKEN_DURATION_DAYS)
                elif values["scope"] == "access":
                    values["exp"] = iat + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)
            return values