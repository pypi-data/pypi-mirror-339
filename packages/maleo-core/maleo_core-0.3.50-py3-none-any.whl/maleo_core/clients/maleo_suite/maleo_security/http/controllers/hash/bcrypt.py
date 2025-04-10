from maleo_core.clients.maleo_suite.maleo_security.http.manager import MaleoSecurityHTTPClientManager
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.hash.bcrypt import MaleoSecurityBcryptHashGeneralParameters

class MaleoSecurityBcryptHashHTTPController:
    @staticmethod
    async def hash(parameters:MaleoSecurityBcryptHashGeneralParameters.Hash) -> BaseHTTPClientControllerResults:
        """Hash a message"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/hash/bcrypt/hash"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, headers=headers, json=json)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def verify(parameters:MaleoSecurityBcryptHashGeneralParameters.Verify) -> BaseHTTPClientControllerResults:
        """verify a message's hash"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/hash/bcrypt/verify"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, headers=headers, json=json)
            return BaseHTTPClientControllerResults(response=response)