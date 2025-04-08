from __future__ import annotations
from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user import MaleoAccessUserQueryResults

class MaleoAccessUserServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-USR-001"
        message:str = "No user(s) found"
        description:str = "External error: No user(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "ACC-USR-002"
        message:str = "Users found"
        description:str = "Requested users found in database"
        data:list[MaleoAccessUserQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-USR-003"
        message:str = "User found"
        description:str = "Requested user found in database"
        data:MaleoAccessUserQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-USR-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-USR-005"
        message:str = "Failed creating user"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-USR-006"
        message:str = "Succesfully created new user"
        description:str = "A new user is created with data provided on request"
        data:MaleoAccessUserQueryResults.Get

    class UpdateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-USR-007"
        message:str = "Failed updating user"

    class UpdateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-USR-008"
        message:str = "Succesfully updated user"
        data:MaleoAccessUserQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No user(s) found Response",
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

    update_responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Update failed response",
            "model": UpdateFailedResponse
        },
        **not_found_responses,
        **BaseGeneralResponsesSchemas.other_responses
    }