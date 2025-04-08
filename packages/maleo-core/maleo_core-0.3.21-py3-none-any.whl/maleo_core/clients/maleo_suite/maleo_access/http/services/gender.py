from typing import Union
from maleo_core.clients.maleo_suite.maleo_access.http.controllers.gender import MaleoAccessGenderHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.gender import MaleoAccessGenderClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.gender import MaleoAccessGenderGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.client.http.services.gender import MaleoAccessHTTPClientGenderServiceResults

class MaleoAccessGenderHTTPService:
    @staticmethod
    async def get_genders(
        parameters:MaleoAccessGenderClientParameters.Get
    ) -> Union[
        MaleoAccessHTTPClientGenderServiceResults.Fail,
        MaleoAccessHTTPClientGenderServiceResults.MultipleData
    ]:
        """Fetch genders from maleo-access"""
        result = await MaleoAccessGenderHTTPController.get_genders(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientGenderServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientGenderServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_gender(
        parameters:MaleoAccessGenderGeneralParameters.GetSingle
    ) -> Union[
        MaleoAccessHTTPClientGenderServiceResults.Fail,
        MaleoAccessHTTPClientGenderServiceResults.SingleData
    ]:
        """Fetch gender from maleo-access"""
        result = await MaleoAccessGenderHTTPController.get_gender(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientGenderServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientGenderServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoAccessGenderGeneralParameters.CreateOrUpdate) -> Union[
        MaleoAccessHTTPClientGenderServiceResults.Fail,
        MaleoAccessHTTPClientGenderServiceResults.SingleData
    ]:
        """Create new gender"""
        result = await MaleoAccessGenderHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientGenderServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientGenderServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        gender_id:int,
        parameters:MaleoAccessGenderGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoAccessHTTPClientGenderServiceResults.Fail,
        MaleoAccessHTTPClientGenderServiceResults.SingleData
    ]:
        """Update gender's data"""
        result = await MaleoAccessGenderHTTPController.update(gender_id=gender_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientGenderServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientGenderServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        gender_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoAccessHTTPClientGenderServiceResults.Fail,
        MaleoAccessHTTPClientGenderServiceResults.SingleData
    ]:
        """Update gender's status"""
        result = await MaleoAccessGenderHTTPController.status_update(gender_id=gender_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientGenderServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientGenderServiceResults.SingleData.model_validate(result.content)