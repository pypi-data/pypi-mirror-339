from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.maleo_suite.maleo_security.transfers.general.secret import MaleoSecuritySecretGeneralTransfers

class MaleoSecuritySecretServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SEC-SCR-001"
        message:str = "No secret(s) found"
        description:str = "External error: No secret(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-SCR-002"
        message:str = "Secret found"
        description:str = "Requested secret found in database"
        data:MaleoSecuritySecretGeneralTransfers.Results

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SEC-SCR-003"
        message:str = "Failed creating secret"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SEC-SCR-004"
        message:str = "Succesfully created new secret"
        description:str = "A new secret is created with data provided on request"
        data:MaleoSecuritySecretGeneralTransfers.Results

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No secret(s) found Response",
            "model": NotFoundResponse
        }
    }

    get_responses={
        **not_found_responses,
        **BaseGeneralResponsesSchemas.other_responses
    }

    create_responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Create failed response",
            "model": CreateFailedResponse
        },
        **BaseGeneralResponsesSchemas.other_responses
    }