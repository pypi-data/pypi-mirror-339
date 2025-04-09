from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.maleo_suite.maleo_security.transfers.general.hash import MaleoSecurityHashGeneralTransfers
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.hash import MaleoSecurityHashGeneralResults

class MaleoSecurityHashServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class HashResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-HSH-001"
        message:str = "Succesfully hashed given message"
        description:str = "A new hash is generated from request"
        data:MaleoSecurityHashGeneralTransfers.Hash

    class VerifyResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-HSH-002"
        message:str = "Succesfully verified hash"
        description:str = "The message and hash has been verified"
        data:MaleoSecurityHashGeneralResults.IsValid