from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.encryption.rsa import MaleoSecurityRSAEncryptionGeneralResults

class MaleoSecurityRSAEncryptionServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class EncryptSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-ENC-RSA-001"
        message:str = "Succesfully encrypted single plaintext"
        description:str = "The given plaintext successfully encrypted with RSA encryption algorithm"
        data:MaleoSecurityRSAEncryptionGeneralResults.EncryptSingle

    class EncryptMultipleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-ENC-RSA-002"
        message:str = "Succesfully encrypted multiple plaintexts"
        description:str = "The given plaintexts successfully encrypted with RSA encryption algorithm"
        data:MaleoSecurityRSAEncryptionGeneralResults.EncryptMultiple

    class DecryptSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-ENC-RSA-003"
        message:str = "Succesfully decrypted single ciphertext"
        description:str = "The given ciphertext successfully decrypted with RSA decryption algorithm"
        data:MaleoSecurityRSAEncryptionGeneralResults.DecryptSingle

    class DecryptMultipleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-ENC-RSA-004"
        message:str = "Succesfully decrypted multiple ciphertexts"
        description:str = "The given ciphertexts successfully decrypted with RSA decryption algorithm"
        data:MaleoSecurityRSAEncryptionGeneralResults.DecryptMultiple