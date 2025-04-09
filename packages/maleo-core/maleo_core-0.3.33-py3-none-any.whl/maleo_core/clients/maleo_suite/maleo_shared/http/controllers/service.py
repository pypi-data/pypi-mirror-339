from maleo_core.clients.maleo_suite.maleo_shared.http.manager import MaleoSharedHTTPClientManager
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_shared.transfers.parameters.client.service import MaleoSharedServiceClientParameters
from maleo_core.models.maleo_suite.maleo_shared.transfers.parameters.general.service import MaleoSharedServiceGeneralParameters

class MaleoSharedServiceHTTPController:
    @staticmethod
    async def get_services(
        parameters:MaleoSharedServiceClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch services from maleo-shared"""
        async with MaleoSharedHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSharedHTTPClientManager._base_url}/v1/services/"

            query_parameters = MaleoSharedServiceClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_service(
        parameters:MaleoSharedServiceGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch service from maleo-shared"""
        async with MaleoSharedHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSharedHTTPClientManager._base_url}/v1/services/"
            if parameters.identifier == MaleoSharedServiceGeneralParameters.UniqueIdentifiers.ID:
                url += f"{parameters.value}"
            else:
                url += f"{parameters.identifier.value}/{parameters.value}"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)