from __future__ import annotations
from pydantic import model_validator
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas

class BaseServiceResponsesSchemas:
    Fail = BaseGeneralResponsesSchemas.Fail
    SingleData = BaseGeneralResponsesSchemas.SingleData
    class MultipleData(BaseGeneralResponsesSchemas.MultipleData):
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