from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_shared.transfers.results.query.service import MaleoSharedServiceQueryResults

class MaleoSharedServiceServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SHA-SYS-001"
        message:str = "No service(s) found"
        description:str = "External error: No service(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "SHA-SYS-002"
        message:str = "Services found"
        description:str = "Requested services found in database"
        data:list[MaleoSharedServiceQueryResults.Get]

    class GetSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "SHA-SYS-003"
        message:str = "Service found"
        description:str = "Requested service found in database"
        data:MaleoSharedServiceQueryResults.Get

    class CheckFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "SHA-SYS-004"

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No services found Response",
            "model": NotFoundResponse
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Internal Server Error Response",
            "model": BaseGeneralResponsesSchemas.ServerError
        }
    }

    check_responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Check failed response",
            "model": CheckFailedResponse
        },
        **not_found_responses
    }

    get_single_responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Get service failed response",
            "model": CheckFailedResponse
        },
        **not_found_responses
    }