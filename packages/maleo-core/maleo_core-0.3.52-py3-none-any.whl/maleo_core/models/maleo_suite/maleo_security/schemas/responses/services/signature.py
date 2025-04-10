from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.maleo_suite.maleo_security.transfers.general.signature import MaleoSecuritySignatureGeneralTransfers
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.signature import MaleoSecuritySignatureGeneralResults

class MaleoSecuritySignatureServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class SignSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-SGN-001"
        message:str = "Succesfully signed single message"
        description:str = "The given message successfully signed"
        data:MaleoSecuritySignatureGeneralTransfers.SignaturePackage

    class SignMultipleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-SGN-002"
        message:str = "Succesfully signed multiple messages"
        description:str = "The given messages successfully signed"
        data:list[MaleoSecuritySignatureGeneralTransfers.SignaturePackage]

    class VerifySingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-SGN-003"
        message:str = "Succesfully verified single signature"
        description:str = "The given signature successfully verified"
        data:MaleoSecuritySignatureGeneralResults.Base

    class VerifyMultipleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-SGN-004"
        message:str = "Succesfully verified multiple signatures"
        description:str = "The given signatures successfully verified"
        data:list[MaleoSecuritySignatureGeneralResults.Base]