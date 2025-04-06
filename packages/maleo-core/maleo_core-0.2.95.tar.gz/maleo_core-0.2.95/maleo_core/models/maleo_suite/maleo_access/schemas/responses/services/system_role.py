from __future__ import annotations
from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.system_role import MaleoAccessSystemRoleQueryResults

class MaleoAccessSystemRoleServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-SYR-001"
        message:str = "No system role(s) found"
        description:str = "External error: No system role(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "ACC-SYR-002"
        message:str = "System roles found"
        description:str = "Requested system roles found in database"
        data:list[MaleoAccessSystemRoleQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-SYR-003"
        message:str = "System role found"
        description:str = "Requested system role found in database"
        data:MaleoAccessSystemRoleQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-SYR-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-SYR-005"
        message:str = "Failed creating system role"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-SYR-006"
        message:str = "Succesfully created new system role"
        description:str = "A new system role is created with data provided on request"
        data:MaleoAccessSystemRoleQueryResults.Get

    class UpdateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-SYR-007"
        message:str = "Failed updating system role"

    class UpdateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-SYR-008"
        message:str = "Succesfully updated system role"
        data:MaleoAccessSystemRoleQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No system role(s) found Response",
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