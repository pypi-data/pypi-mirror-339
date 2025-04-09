from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.encryption.aes import MaleoSecurityAESEncryptionGeneralResults

class MaleoSecurityAESEncryptionServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class EncryptSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-ENC-AES-001"
        message:str = "Succesfully encrypted single plaintext"
        description:str = "The given plaintext successfully encrypted with AES encryption algorithm"
        data:MaleoSecurityAESEncryptionGeneralResults.EncryptSingle

    class EncryptMultipleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-ENC-AES-002"
        message:str = "Succesfully encrypted multiple plaintexts"
        description:str = "The given plaintexts successfully encrypted with AES encryption algorithm"
        data:MaleoSecurityAESEncryptionGeneralResults.EncryptMultiple

    class DecryptSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-ENC-AES-003"
        message:str = "Succesfully decrypted single ciphertext"
        description:str = "The given ciphertext successfully decrypted with AES decryption algorithm"
        data:MaleoSecurityAESEncryptionGeneralResults.DecryptSingle

    class DecryptMultipleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-ENC-AES-004"
        message:str = "Succesfully decrypted multiple ciphertexts"
        description:str = "The given ciphertexts successfully decrypted with AES decryption algorithm"
        data:MaleoSecurityAESEncryptionGeneralResults.DecryptMultiple