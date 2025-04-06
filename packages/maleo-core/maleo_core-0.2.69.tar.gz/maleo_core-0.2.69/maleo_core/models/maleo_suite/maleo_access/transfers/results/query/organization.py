from __future__ import annotations
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.organization import MaleoAccessOrganizationGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.organization_type import MaleoAccessOrganizationTypeQueryResults

class MaleoAccessOrganizationQueryResults:
    class ParentOrganization(MaleoAccessOrganizationGeneralTransfers.Base, BaseServiceQueryResults.Get): pass

    class Get(MaleoAccessOrganizationGeneralTransfers.Base, BaseServiceQueryResults.Get):
        organization_type:MaleoAccessOrganizationTypeQueryResults.Get = Field(..., description="Organization's type")
        parent_organization:Optional[MaleoAccessOrganizationQueryResults.ParentOrganization] = Field(None, description="Parent's organization")

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessOrganizationQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessOrganizationQueryResults.Get]

MaleoAccessOrganizationQueryResults.Get.model_rebuild()