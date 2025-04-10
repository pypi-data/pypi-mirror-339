from maleo_core.clients.maleo_suite.maleo_security.http.manager import MaleoSecurityHTTPClientManager
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.key import MaleoSecurityKeyGeneralParameters

class MaleoSecurityKeyHTTPController:
    @staticmethod
    async def generate_private(parameters:MaleoSecurityKeyGeneralParameters.GeneratePairOrPrivate) -> BaseHTTPClientControllerResults:
        """Generate private key"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/keys/private"

            params = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def generate_public(parameters:MaleoSecurityKeyGeneralParameters.GeneratePublic) -> BaseHTTPClientControllerResults:
        """Generate public key"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/keys/public"

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
    async def generate_pair(parameters:MaleoSecurityKeyGeneralParameters.GeneratePairOrPrivate) -> BaseHTTPClientControllerResults:
        """Generate key pair"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/keys/pair"

            params = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)