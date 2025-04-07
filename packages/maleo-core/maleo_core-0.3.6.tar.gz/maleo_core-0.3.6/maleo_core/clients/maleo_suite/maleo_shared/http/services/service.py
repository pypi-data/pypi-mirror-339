from typing import Union
from maleo_core.clients.maleo_suite.maleo_shared.http.controllers.service import MaleoSharedServiceHTTPController
from maleo_core.models.maleo_suite.maleo_shared.transfers.parameters.client.service import MaleoSharedServiceClientParameters
from maleo_core.models.maleo_suite.maleo_shared.transfers.parameters.general.service import MaleoSharedServiceGeneralParameters
from maleo_core.models.maleo_suite.maleo_shared.transfers.results.client.http.services.service import MaleoSharedHTTPClientServiceServiceResults

class MaleoSharedServiceHTTPService:
    @staticmethod
    async def get_services(
        parameters:MaleoSharedServiceClientParameters.Get
    ) -> Union[
        MaleoSharedHTTPClientServiceServiceResults.Fail,
        MaleoSharedHTTPClientServiceServiceResults.MultipleData
    ]:
        """Fetch services from maleo-shared"""
        result = await MaleoSharedServiceHTTPController.get_services(parameters=parameters)
        if not result.success:
            return MaleoSharedHTTPClientServiceServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSharedHTTPClientServiceServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_service(
        parameters:MaleoSharedServiceGeneralParameters.GetSingle
    ) -> Union[
        MaleoSharedHTTPClientServiceServiceResults.Fail,
        MaleoSharedHTTPClientServiceServiceResults.SingleData
    ]:
        """Fetch service from maleo-shared"""
        result = await MaleoSharedServiceHTTPController.get_service(parameters=parameters)
        if not result.success:
            return MaleoSharedHTTPClientServiceServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoSharedHTTPClientServiceServiceResults.SingleData.model_validate(result.content)