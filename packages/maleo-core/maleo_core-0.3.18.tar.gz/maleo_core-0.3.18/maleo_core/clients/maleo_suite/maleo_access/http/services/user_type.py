from typing import Union
from maleo_core.clients.maleo_suite.maleo_access.http.controllers.user_type import MaleoAccessUserTypeHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_type import MaleoAccessUserTypeGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.client.http.services.user_type import MaleoAccessHTTPClientUserTypeServiceResults

class MaleoAccessUserTypeHTTPService:
    @staticmethod
    async def get_user_type(
        parameters:MaleoAccessUserTypeGeneralParameters.GetSingle
    ) -> Union[
        MaleoAccessHTTPClientUserTypeServiceResults.Fail,
        MaleoAccessHTTPClientUserTypeServiceResults.SingleData
    ]:
        """Fetch user type from maleo-access"""
        result = await MaleoAccessUserTypeHTTPController.get_user_type(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserTypeServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoAccessUserTypeGeneralParameters.CreateOrUpdate) -> Union[
        MaleoAccessHTTPClientUserTypeServiceResults.Fail,
        MaleoAccessHTTPClientUserTypeServiceResults.SingleData
    ]:
        """Create new user type"""
        result = await MaleoAccessUserTypeHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserTypeServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        user_type_id:int,
        parameters:MaleoAccessUserTypeGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoAccessHTTPClientUserTypeServiceResults.Fail,
        MaleoAccessHTTPClientUserTypeServiceResults.SingleData
    ]:
        """Update user type's data"""
        result = await MaleoAccessUserTypeHTTPController.update(user_type_id=user_type_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserTypeServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        user_type_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoAccessHTTPClientUserTypeServiceResults.Fail,
        MaleoAccessHTTPClientUserTypeServiceResults.SingleData
    ]:
        """Update user type's status"""
        result = await MaleoAccessUserTypeHTTPController.status_update(user_type_id=user_type_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientUserTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientUserTypeServiceResults.SingleData.model_validate(result.content)