from typing import Union
from maleo_core.clients.maleo_suite.maleo_access.http.controllers.blood_type import MaleoAccessBloodTypeHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.blood_type import MaleoAccessBloodTypeClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.blood_type import MaleoAccessBloodTypeGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.client.http.services.blood_type import MaleoAccessHTTPClientBloodTypeServiceResults

class MaleoAccessBloodTypeHTTPService:
    @staticmethod
    async def get_blood_types(
        parameters:MaleoAccessBloodTypeClientParameters.Get
    ) -> Union[
        MaleoAccessHTTPClientBloodTypeServiceResults.Fail,
        MaleoAccessHTTPClientBloodTypeServiceResults.MultipleData
    ]:
        """Fetch blood types from maleo-access"""
        result = await MaleoAccessBloodTypeHTTPController.get_blood_types(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientBloodTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientBloodTypeServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_blood_type(
        parameters:MaleoAccessBloodTypeGeneralParameters.GetSingle
    ) -> Union[
        MaleoAccessHTTPClientBloodTypeServiceResults.Fail,
        MaleoAccessHTTPClientBloodTypeServiceResults.SingleData
    ]:
        """Fetch blood type from maleo-access"""
        result = await MaleoAccessBloodTypeHTTPController.get_blood_type(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientBloodTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientBloodTypeServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoAccessBloodTypeGeneralParameters.CreateOrUpdate) -> Union[
        MaleoAccessHTTPClientBloodTypeServiceResults.Fail,
        MaleoAccessHTTPClientBloodTypeServiceResults.SingleData
    ]:
        """Create new blood type"""
        result = await MaleoAccessBloodTypeHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientBloodTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientBloodTypeServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        blood_type_id:int,
        parameters:MaleoAccessBloodTypeGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoAccessHTTPClientBloodTypeServiceResults.Fail,
        MaleoAccessHTTPClientBloodTypeServiceResults.SingleData
    ]:
        """Update blood type's data"""
        result = await MaleoAccessBloodTypeHTTPController.update(blood_type_id=blood_type_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientBloodTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientBloodTypeServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        blood_type_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoAccessHTTPClientBloodTypeServiceResults.Fail,
        MaleoAccessHTTPClientBloodTypeServiceResults.SingleData
    ]:
        """Update blood type's status"""
        result = await MaleoAccessBloodTypeHTTPController.status_update(blood_type_id=blood_type_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientBloodTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientBloodTypeServiceResults.SingleData.model_validate(result.content)