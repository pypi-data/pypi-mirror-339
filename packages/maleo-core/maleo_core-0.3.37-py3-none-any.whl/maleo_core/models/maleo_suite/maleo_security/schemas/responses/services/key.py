from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.key import MaleoSecurityKeyGeneralResults

class MaleoSecurityKeyServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class GeneratePrivateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-KEY-001"
        message:str = "Succesfully generated new private key"
        description:str = "A new private key is generated with data provided on request"
        data:MaleoSecurityKeyGeneralResults.GeneratePrivate

    class GeneratePublicSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-KEY-002"
        message:str = "Succesfully generated new public key"
        description:str = "A new public key is generated with data provided on request"
        data:MaleoSecurityKeyGeneralResults.GeneratePublic

    class GeneratePairSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-KEY-003"
        message:str = "Succesfully generated new key pair"
        description:str = "A new key pair is generated with data provided on request"
        data:MaleoSecurityKeyGeneralResults.GeneratePair