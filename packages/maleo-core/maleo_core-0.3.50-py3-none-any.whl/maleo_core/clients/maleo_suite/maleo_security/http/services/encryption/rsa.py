from typing import Union
from maleo_core.clients.maleo_suite.maleo_security.http.controllers.encryption.rsa import MaleoSecurityRSAEncryptionHTTPController
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.encryption.rsa import MaleoSecurityRSAEncryptionGeneralParameters
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.encryption.rsa import MaleoSecurityRSAEncryptionGeneralResults

class MaleoSecurityRSAEncryptionHTTPService:
    @staticmethod
    async def encrypt_single(
        parameters:MaleoSecurityRSAEncryptionGeneralParameters.EncryptSingle
    ) -> Union[
        MaleoSecurityRSAEncryptionGeneralResults.Fail,
        MaleoSecurityRSAEncryptionGeneralResults.SingleEncryption
    ]:
        """Encrypt single plaintext"""
        result = await MaleoSecurityRSAEncryptionHTTPController.encrypt_single(parameters=parameters)
        if not result.success:
            return MaleoSecurityRSAEncryptionGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityRSAEncryptionGeneralResults.SingleEncryption.model_validate(result.content)

    @staticmethod
    async def encrypt_multiple(
        parameters:MaleoSecurityRSAEncryptionGeneralParameters.EncryptMultiple
    ) -> Union[
        MaleoSecurityRSAEncryptionGeneralResults.Fail,
        MaleoSecurityRSAEncryptionGeneralResults.MultipleEncryption
    ]:
        """Encrypt multiple plaintexts"""
        result = await MaleoSecurityRSAEncryptionHTTPController.encrypt_multiple(parameters=parameters)
        if not result.success:
            return MaleoSecurityRSAEncryptionGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityRSAEncryptionGeneralResults.MultipleEncryption.model_validate(result.content)

    @staticmethod
    async def decrypt_single(
        parameters:MaleoSecurityRSAEncryptionGeneralParameters.DecryptSingle
    ) -> Union[
        MaleoSecurityRSAEncryptionGeneralResults.Fail,
        MaleoSecurityRSAEncryptionGeneralResults.SingleDecryption
    ]:
        """Decrypt single ciphertext"""
        result = await MaleoSecurityRSAEncryptionHTTPController.decrypt_single(parameters=parameters)
        if not result.success:
            return MaleoSecurityRSAEncryptionGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityRSAEncryptionGeneralResults.SingleDecryption.model_validate(result.content)

    @staticmethod
    async def decrypt_multiple(
        parameters:MaleoSecurityRSAEncryptionGeneralParameters.DecryptMultiple
    ) -> Union[
        MaleoSecurityRSAEncryptionGeneralResults.Fail,
        MaleoSecurityRSAEncryptionGeneralResults.MultipleDecryption
    ]:
        """Decrypt multiple ciphertexts"""
        result = await MaleoSecurityRSAEncryptionHTTPController.decrypt_multiple(parameters=parameters)
        if not result.success:
            return MaleoSecurityRSAEncryptionGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityRSAEncryptionGeneralResults.MultipleDecryption.model_validate(result.content)