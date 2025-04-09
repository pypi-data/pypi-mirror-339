from __future__ import annotations
import re
import urllib.parse
from datetime import datetime
from pydantic import field_validator, model_validator
from typing import Self
from maleo_core.models.base.general import BaseGeneralModels
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.utils.constants import SORT_COLUMN_PATTERN, DATE_FILTER_PATTERN

class BaseServiceParameters:
    class GetQuery(
        BaseGeneralParameters.Filters,
        BaseGeneralParameters.Sorts,
        BaseGeneralParameters.Search,
        BaseGeneralModels.SimplePagination,
        BaseGeneralParameters.Statuses
    ):
        @field_validator("sort")
        @classmethod
        def validate_sort_columns(cls, values):
            if not isinstance(values, list):
                return ["id.asc"]
            return [value for value in values if SORT_COLUMN_PATTERN.match(value)]

        @field_validator("filter")
        @classmethod
        def validate_date_filters(cls, values):
            if isinstance(values, list):
                decoded_values = [urllib.parse.unquote(value) for value in values]
                #* Replace space followed by 2 digits, colon, 2 digits with + and those digits
                fixed_values = []
                for value in decoded_values:
                    #* Look for the pattern: space followed by 2 digits, colon, 2 digits
                    fixed_value = re.sub(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+) (\d{2}:\d{2})', r'\1+\2', value)
                    fixed_values.append(fixed_value)
                final_values = [value for value in fixed_values if DATE_FILTER_PATTERN.match(value)]
                return final_values

    class Get(
        BaseGeneralParameters.DateFilters,
        BaseGeneralParameters.SortColumns,
        GetQuery
    ):
        @model_validator(mode="after")
        def set_sort_columns(self) -> Self:
            #* Process sort parameters
            sort_columns = []
            for item in self.sort:
                parts = item.split('.')
                if len(parts) == 2 and parts[1].lower() in ["asc", "desc"]:
                    try:
                        sort_columns.append(BaseGeneralModels.SortColumn(name=parts[0], order=BaseGeneralModels.SortOrder(parts[1].lower())))
                    except ValueError:
                        continue

            #* Only update if we have valid sort columns, otherwise keep the default
            if sort_columns:
                self.sort_columns = sort_columns
            return self

        @model_validator(mode="after")
        def set_date_filters(self) -> Self:
            #* Process filter parameters
            date_filters = []
            for filter_item in self.filter:
                parts = filter_item.split('|')
                if len(parts) >= 2 and parts[0]:
                    name = parts[0]
                    from_date = None
                    to_date = None

                    #* Process each part to extract from and to dates
                    for part in parts[1:]:
                        if part.startswith('from::'):
                            try:
                                from_date_str = part.replace('from::', '')
                                from_date = datetime.fromisoformat(from_date_str)
                            except ValueError:
                                continue
                        elif part.startswith('to::'):
                            try:
                                to_date_str = part.replace('to::', '')
                                to_date = datetime.fromisoformat(to_date_str)
                            except ValueError:
                                continue

                    #* Only add filter if at least one date is specified
                    if from_date or to_date:
                        date_filters.append(BaseGeneralModels.DateFilter(name=name, from_date=from_date, to_date=to_date))

            #* Update date_filters
            self.date_filters = date_filters
            return self