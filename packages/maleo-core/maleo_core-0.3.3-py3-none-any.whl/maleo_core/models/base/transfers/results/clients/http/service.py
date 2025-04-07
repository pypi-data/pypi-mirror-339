from __future__ import annotations
from pydantic import model_validator
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.base.transfers.results.general import BaseGeneralResults

class BaseHTTPClientServiceResults:
    Fail = BaseGeneralResults.Fail
    SingleData = BaseGeneralResults.SingleData
    class MultipleData(BaseGeneralResults.MultipleData):
        @model_validator(mode="before")
        @classmethod
        def calculate_pagination_component(cls, values: dict) -> dict:
            """Extracts pagination components (page, limit, total_data) before validation."""
            pagination = values.get("pagination")

            if isinstance(pagination, BaseGeneralModels.ExtendedPagination):
                values["page"] = pagination.page
                values["limit"] = pagination.limit
                values["total_data"] = pagination.total_data

            return values