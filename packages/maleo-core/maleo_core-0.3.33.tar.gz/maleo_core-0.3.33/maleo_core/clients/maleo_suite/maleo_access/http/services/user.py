from typing import Union
from maleo_core.clients.maleo_suite.maleo_access.http.controllers.user import MaleoAccessUserHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.user import MaleoAccessUserClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user import MaleoAccessUserGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.client.http.services.user import MaleoAccessHTTPClientUserServiceResults

class MaleoAccessUserHTTPService:
    @staticmethod
    async def get_users(
        parameters:MaleoAccessUserClientParameters.Get
    ) -> Union[
        MaleoAccessHTTPClientUserServiceResults.Fail,
        MaleoAccessHTTPClientUserServiceResults.MultipleData
    ]:
        """Fetch users from maleo-access"""
        result = await MaleoAccessUserHTTPController.get_users(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_user(
        parameters:MaleoAccessUserGeneralParameters.GetSingle
    ) -> Union[
        MaleoAccessHTTPClientUserServiceResults.Fail,
        MaleoAccessHTTPClientUserServiceResults.SingleData
    ]:
        """Fetch user from maleo-access"""
        result = await MaleoAccessUserHTTPController.get_user(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserServiceResults.SingleData.model_validate(result.content)

    # @staticmethod
    # async def create(parameters:MaleoAccessUserGeneralParameters.CreateOrUpdate) -> Union[
    #     MaleoAccessHTTPClientUserServiceResults.Fail,
    #     MaleoAccessHTTPClientUserServiceResults.SingleData
    # ]:
    #     """Create new user"""
    #     result = await MaleoAccessUserHTTPController.create(parameters=parameters)
    #     if not result.success:
    #         return MaleoAccessHTTPClientUserServiceResults.Fail.model_validate(result.content)
    #     else:
    #         return MaleoAccessHTTPClientUserServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        user_id:int,
        parameters:MaleoAccessUserGeneralParameters.Update
    ) -> Union[
        MaleoAccessHTTPClientUserServiceResults.Fail,
        MaleoAccessHTTPClientUserServiceResults.SingleData
    ]:
        """Update user's data"""
        result = await MaleoAccessUserHTTPController.update(user_id=user_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        user_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoAccessHTTPClientUserServiceResults.Fail,
        MaleoAccessHTTPClientUserServiceResults.SingleData
    ]:
        """Update user's status"""
        result = await MaleoAccessUserHTTPController.status_update(user_id=user_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserServiceResults.SingleData.model_validate(result.content)