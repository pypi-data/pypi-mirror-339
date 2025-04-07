from __future__ import annotations
from fastapi.responses import JSONResponse
from pydantic import BaseModel, model_validator
from typing import Optional
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.base.transfers.results.general import BaseGeneralResults
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults

class BaseServiceGeneralResults:
    class Authorization(BaseModel):
        authorized:bool
        response:Optional[JSONResponse] = None
        token:Optional[str] = None

        class Config:
            arbitrary_types_allowed = True

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