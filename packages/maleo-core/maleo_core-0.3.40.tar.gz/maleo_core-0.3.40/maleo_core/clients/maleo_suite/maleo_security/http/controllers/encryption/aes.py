from maleo_core.clients.maleo_suite.maleo_security.http.manager import MaleoSecurityHTTPClientManager
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.encryption.aes import MaleoSecurityAESEncryptionGeneralParameters

class MaleoSecurityAESEncryptionHTTPController:
    @staticmethod
    async def encrypt_single(parameters:MaleoSecurityAESEncryptionGeneralParameters.EncryptSingle) -> BaseHTTPClientControllerResults:
        """Encrypt single plaintext"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/encryptions/aes/encrypt/single"

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
    async def encrypt_multiple(parameters:MaleoSecurityAESEncryptionGeneralParameters.EncryptMultiple) -> BaseHTTPClientControllerResults:
        """Encrypt multiple plaintexts"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/encryptions/aes/encrypt/multiple"

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
    async def decrypt_single(parameters:MaleoSecurityAESEncryptionGeneralParameters.DecryptSingle) -> BaseHTTPClientControllerResults:
        """Decrypt single ciphertext"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/encryptions/aes/decrypt/single"

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
    async def decrypt_multiple(parameters:MaleoSecurityAESEncryptionGeneralParameters.DecryptMultiple) -> BaseHTTPClientControllerResults:
        """Decrypt multiple ciphertexts"""
        async with MaleoSecurityHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager._base_url}/v1/encryptions/aes/decrypt/multiple"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, headers=headers, json=json)
            return BaseHTTPClientControllerResults(response=response)