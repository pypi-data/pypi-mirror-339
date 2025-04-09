from maleo_core.clients.maleo_suite.maleo_security.http.manager import MaleoSecurityHTTPClientManager
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_security.transfers.general.secret import MaleoSecuritySecretGeneralTransfers

class MaleoSecuritySecretHTTPController:
    @staticmethod
    async def get(parameters:MaleoSecuritySecretGeneralTransfers.GetParameters) -> BaseHTTPClientControllerResults:
        """Fetch secret from maleo-security"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/secrets/"

            params = parameters.model_dump()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def create(parameters:MaleoSecuritySecretGeneralTransfers.CreateParameters) -> BaseHTTPClientControllerResults:
        """Create new secret"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/secrets/"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)