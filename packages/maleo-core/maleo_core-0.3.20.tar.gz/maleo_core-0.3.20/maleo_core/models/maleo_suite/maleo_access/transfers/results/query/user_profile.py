from __future__ import annotations
from pydantic import Field
from typing import Optional
from maleo_core.models.base.transfers.results.services.query import BaseServiceQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.general.user_profile import MaleoAccessUserProfileGeneralTransfers
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.gender import MaleoAccessGenderQueryResults
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.blood_type import MaleoAccessBloodTypeQueryResults

class MaleoAccessUserProfileQueryResults:
    class Get(MaleoAccessUserProfileGeneralTransfers.Base, BaseServiceQueryResults.Get):
        gender:Optional[MaleoAccessGenderQueryResults.Get] = Field(..., description="User's gender")
        blood_type:Optional[MaleoAccessBloodTypeQueryResults.Get] = Field(..., description="User's blood type")

    Fail = BaseServiceQueryResults.Fail

    class SingleData(BaseServiceQueryResults.SingleData):
        data:Optional[MaleoAccessUserProfileQueryResults.Get]

    class MultipleData(BaseServiceQueryResults.MultipleData):
        data:list[MaleoAccessUserProfileQueryResults.Get]