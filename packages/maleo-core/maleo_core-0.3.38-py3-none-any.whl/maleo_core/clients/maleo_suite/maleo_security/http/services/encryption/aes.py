from typing import Union
from maleo_core.clients.maleo_suite.maleo_security.http.controllers.encryption.aes import MaleoSecurityAESEncryptionHTTPController
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.encryption.aes import MaleoSecurityAESEncryptionGeneralParameters
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.encryption.aes import MaleoSecurityAESEncryptionGeneralResults

class MaleoSecurityAESEncryptionHTTPService:
    @staticmethod
    async def encrypt_single(
        parameters:MaleoSecurityAESEncryptionGeneralParameters.EncryptSingle
    ) -> Union[
        MaleoSecurityAESEncryptionGeneralResults.Fail,
        MaleoSecurityAESEncryptionGeneralResults.SingleEncryption
    ]:
        """Encrypt single plaintext"""
        result = await MaleoSecurityAESEncryptionHTTPController.encrypt_single(parameters=parameters)
        if not result.success:
            return MaleoSecurityAESEncryptionGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityAESEncryptionGeneralResults.SingleEncryption.model_validate(result.content)

    @staticmethod
    async def encrypt_multiple(
        parameters:MaleoSecurityAESEncryptionGeneralParameters.EncryptMultiple
    ) -> Union[
        MaleoSecurityAESEncryptionGeneralResults.Fail,
        MaleoSecurityAESEncryptionGeneralResults.MultipleEncryption
    ]:
        """Encrypt multiple plaintexts"""
        result = await MaleoSecurityAESEncryptionHTTPController.encrypt_multiple(parameters=parameters)
        if not result.success:
            return MaleoSecurityAESEncryptionGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityAESEncryptionGeneralResults.MultipleEncryption.model_validate(result.content)

    @staticmethod
    async def decrypt_single(
        parameters:MaleoSecurityAESEncryptionGeneralParameters.DecryptSingle
    ) -> Union[
        MaleoSecurityAESEncryptionGeneralResults.Fail,
        MaleoSecurityAESEncryptionGeneralResults.SingleDecryption
    ]:
        """Decrypt single ciphertext"""
        result = await MaleoSecurityAESEncryptionHTTPController.decrypt_single(parameters=parameters)
        if not result.success:
            return MaleoSecurityAESEncryptionGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityAESEncryptionGeneralResults.SingleDecryption.model_validate(result.content)

    @staticmethod
    async def decrypt_multiple(
        parameters:MaleoSecurityAESEncryptionGeneralParameters.DecryptMultiple
    ) -> Union[
        MaleoSecurityAESEncryptionGeneralResults.Fail,
        MaleoSecurityAESEncryptionGeneralResults.MultipleDecryption
    ]:
        """Decrypt multiple ciphertexts"""
        result = await MaleoSecurityAESEncryptionHTTPController.decrypt_multiple(parameters=parameters)
        if not result.success:
            return MaleoSecurityAESEncryptionGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityAESEncryptionGeneralResults.MultipleDecryption.model_validate(result.content)