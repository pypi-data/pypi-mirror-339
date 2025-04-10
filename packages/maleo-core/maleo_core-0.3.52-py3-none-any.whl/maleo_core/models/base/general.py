from __future__ import annotations
from datetime import date, datetime, timedelta, timezone
from enum import StrEnum
from pydantic import BaseModel, Field, model_validator, field_serializer, FieldSerializationInfo
from typing import Dict, List, Literal, Optional, Union, Any
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

    class TokenType(StrEnum):
        REFRESH = "refresh"
        ACCESS = "access"

    class Token(BaseModel):
        type:BaseGeneralModels.TokenType
        sr:UUID
        u:UUID
        o:Optional[UUID]
        uor:Optional[UUID]
        iat:datetime = datetime.now(timezone.utc)
        exp:datetime

        @model_validator(mode="before")
        @classmethod
        def set_iat_and_exp(cls, values:dict):
            iat = values.get("iat", None)
            exp = values.get("iat", None)
            if not iat:
                iat = datetime.now(timezone.utc)
                values["iat"] = iat
            if not exp:
                iat = datetime.now(timezone.utc)
                values["iat"] = iat
                if values["scope"] == BaseGeneralModels.TokenType.REFRESH:
                    values["exp"] = iat + timedelta(days=REFRESH_TOKEN_DURATION_DAYS)
                elif values["scope"] == BaseGeneralModels.TokenType.ACCESS:
                    values["exp"] = iat + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)
            return values
        
        @field_serializer('*')
        def serialize_fields(self, value, info:FieldSerializationInfo) -> Any:
            """Serializes all unique-typed fields."""
            if isinstance(value, UUID):
                return str(value)
            if isinstance(value, datetime) or isinstance(value, date):
                return value.isoformat()
            return value