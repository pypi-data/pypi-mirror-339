from __future__ import annotations
from datetime import datetime, date
from pydantic import field_validator, field_serializer, model_validator
from pydantic_core.core_schema import FieldSerializationInfo
from typing import Optional, Any
from uuid import UUID
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.base.transfers.results.general import BaseGeneralResults

class BaseServiceQueryResults:
    class Get(
        BaseGeneralResults.Status,
        BaseGeneralResults.Timestamp,
        BaseGeneralResults.UniqueIdentifiers
    ):
        @field_validator('*', mode="before")
        def set_none(cls, values):
            if isinstance(values, str) and (values == "" or len(values) == 0):
                return None
            return values
        
        @field_serializer('*')
        def serialize_fields(self, value, info:FieldSerializationInfo) -> Any:
            """Serializes all unique-typed fields."""
            if isinstance(value, UUID):
                return str(value)
            if isinstance(value, datetime) or isinstance(value, date):
                return value.isoformat()
            return value

        class Config:
            from_attributes=True

    Fail = BaseGeneralResults.Fail

    class SingleData(BaseGeneralResults.SingleData):
        data:Optional[BaseServiceQueryResults.Get]

    class MultipleData(BaseGeneralResults.MultipleData):
        data:list[BaseServiceQueryResults.Get]

        @model_validator(mode="before")
        @classmethod
        def calculate_pagination(cls, values: dict) -> dict:
            """Calculates pagination metadata before validation."""
            total_data = values.get("total_data", 0)
            data = values.get("data", [])

            # Get pagination values from inherited SimplePagination
            page = values.get("page", 1)
            limit = values.get("limit", 10)

            # Calculate total pages
            total_pages = (total_data // limit) + (1 if total_data % limit > 0 else 0)

            # Assign computed pagination object before validation
            values["pagination"] = BaseGeneralModels.ExtendedPagination(
                page=page,
                limit=limit,
                data_count=len(data),
                total_data=total_data,
                total_pages=total_pages
            )
            return values