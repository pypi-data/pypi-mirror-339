from typing import Union
from maleo_core.clients.maleo_suite.maleo_access.http.controllers.user_profile import MaleoAccessUserProfileHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.user_profile import MaleoAccessUserProfileClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_profile import MaleoAccessUserProfileGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.client.http.services.user_profile import MaleoAccessHTTPClientUserProfileServiceResults

from maleo_core.clients.maleo_suite.maleo_access.http.manager import MaleoAccessHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_profile import MaleoAccessUserProfileGeneralParameters

class MaleoAccessUserProfileHTTPService:
    @staticmethod
    async def get_user_profile(
        user_id:int,
        parameters:MaleoAccessUserProfileGeneralParameters.GetSingle
    ) -> Union[
        MaleoAccessHTTPClientUserProfileServiceResults.Fail,
        MaleoAccessHTTPClientUserProfileServiceResults.SingleData
    ]:
        """Fetch user's profile from maleo-access"""
        result = await MaleoAccessUserProfileHTTPController.get_user_profile(user_id=user_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserProfileServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserProfileServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(
        user_id:int,
        parameters:MaleoAccessUserProfileGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoAccessHTTPClientUserProfileServiceResults.Fail,
        MaleoAccessHTTPClientUserProfileServiceResults.SingleData
    ]:
        """Create new user's profile"""
        result = await MaleoAccessUserProfileHTTPController.create(user_id=user_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserProfileServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserProfileServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        user_id:int,
        parameters:MaleoAccessUserProfileGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoAccessHTTPClientUserProfileServiceResults.Fail,
        MaleoAccessHTTPClientUserProfileServiceResults.SingleData
    ]:
        """Update user's profile data"""
        result = await MaleoAccessUserProfileHTTPController.update(user_id=user_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserProfileServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserProfileServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        user_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoAccessHTTPClientUserProfileServiceResults.Fail,
        MaleoAccessHTTPClientUserProfileServiceResults.SingleData
    ]:
        """Update user's profile status"""
        result = await MaleoAccessUserProfileHTTPController.status_update(user_id=user_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserProfileServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserProfileServiceResults.SingleData.model_validate(result.content)