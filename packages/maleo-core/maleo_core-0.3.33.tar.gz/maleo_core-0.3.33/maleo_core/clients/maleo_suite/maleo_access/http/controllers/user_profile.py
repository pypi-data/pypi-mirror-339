from maleo_core.clients.maleo_suite.maleo_access.http.manager import MaleoAccessHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.user_profile import MaleoAccessUserProfileGeneralParameters

class MaleoAccessUserProfileHTTPController:
    @staticmethod
    async def get_user_profile(
        user_id:int,
        parameters:MaleoAccessUserProfileGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch user's profile from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/users/{user_id}/profile/"

            #* Construct query parameters
            query_params = BaseGeneralParameters.GetSingleQuery.model_validate(parameters.model_dump())
            params = query_params.model_dump()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def create(
        user_id:int,
        parameters:MaleoAccessUserProfileGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Create new user's profile"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/users/{user_id}/profile/"

            #* Define headers
            headers = {
                "Content-Profile": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def update(
        user_id:int,
        parameters:MaleoAccessUserProfileGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update user's profile data"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/users/{user_id}/profile/"

            #* Define headers
            headers = {
                "Content-Profile": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.put(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def status_update(
        user_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update user's profile status"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/users/{user_id}/profile/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)