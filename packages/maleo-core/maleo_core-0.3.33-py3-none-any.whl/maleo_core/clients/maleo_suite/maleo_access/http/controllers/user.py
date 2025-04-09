from maleo_core.clients.maleo_suite.maleo_access.http.manager import MaleoAccessHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.user import MaleoAccessUserClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user import MaleoAccessUserGeneralParameters

class MaleoAccessUserHTTPController:
    @staticmethod
    async def get_users(
        parameters:MaleoAccessUserClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch users from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/users/"

            query_parameters = MaleoAccessUserClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_user(
        parameters:MaleoAccessUserGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch user from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/users/"
            if parameters.identifier == MaleoAccessUserGeneralParameters.UniqueIdentifiers.ID:
                url += f"{parameters.value}"
            else:
                url += f"{parameters.identifier.value}/{parameters.value}"

            #* Construct query parameters
            query_params = BaseGeneralParameters.GetSingleQuery.model_validate(parameters.model_dump())
            params = query_params.model_dump()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    # @staticmethod
    # async def create(parameters:MaleoAccessUserGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
    #     """Create new user"""
    #     async with MaleoAccessHTTPClientManager.get() as client:
    #         #* Define URL
    #         url = f"{MaleoAccessHTTPClientManager._base_url}/v1/users/"

    #         #* Define headers
    #         headers = {
    #             "Content-Type": "application/json"
    #         }

    #         #* Construct body
    #         json = parameters.model_dump()

    #         #* Get Response
    #         response = await client.post(url=url, json=json, headers=headers)
    #         return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def update(
        user_id:int,
        parameters:MaleoAccessUserGeneralParameters.Update
    ) -> BaseHTTPClientControllerResults:
        """Update user's data"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/users/{user_id}"

            #* Define headers
            headers = {
                "Content-": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.put(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def status_update(
        user_id:int,
        parameters:MaleoAccessUserGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update user's status"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/users/{user_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)