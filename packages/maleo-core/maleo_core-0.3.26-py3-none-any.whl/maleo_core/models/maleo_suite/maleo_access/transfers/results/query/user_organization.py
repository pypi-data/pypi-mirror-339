from __future__ import annotations
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_organization import MaleoAccessUserOrganizationGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.organization import MaleoAccessOrganizationQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user import MaleoAccessUserQueryResults

class MaleoAccessUserOrganizationQueryResults:
    class Get(MaleoAccessUserOrganizationGeneralTransfers.Base, BaseServiceQueryResults.Get):
        user:MaleoAccessUserQueryResults.BaseGet = Field(..., description="User's data")
        organization:MaleoAccessOrganizationQueryResults.Get = Field(..., description="Organization's data")

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessUserOrganizationQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessUserOrganizationQueryResults.Get]