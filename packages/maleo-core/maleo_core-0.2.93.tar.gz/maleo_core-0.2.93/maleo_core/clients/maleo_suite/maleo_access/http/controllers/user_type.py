from maleo_core.clients.maleo_suite.maleo_access.http.manager import MaleoAccessHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.user_type import MaleoAccessUserTypeClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_type import MaleoAccessUserTypeGeneralParameters

class MaleoAccessUserTypeHTTPController:
    @staticmethod
    async def get_user_types(
        parameters:MaleoAccessUserTypeClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch user types from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/user-types/"

            query_parameters = MaleoAccessUserTypeClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_user_type(
        parameters:MaleoAccessUserTypeGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch user type from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/user-types/"
            if parameters.identifier == MaleoAccessUserTypeGeneralParameters.UniqueIdentifiers.ID:
                url += f"{parameters.value}"
            else:
                url += f"{parameters.identifier.value}/{parameters.value}"

            #* Construct query parameters
            query_params = BaseGeneralParameters.GetSingleQuery.model_validate(parameters.model_dump())
            params = query_params.model_dump()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def create(parameters:MaleoAccessUserTypeGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
        """Create new user type"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/user-types/"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def update(
        user_type_id:int,
        parameters:MaleoAccessUserTypeGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update user type's data"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/user-types/{user_type_id}"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.put(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def status_update(
        user_type_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update user type's status"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/user-types/{user_type_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)