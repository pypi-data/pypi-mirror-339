from __future__ import annotations
from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.user_organization_role import MaleoAccessUserOrganizationRoleQueryResults

class MaleoAccessUserOrganizationRoleServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-UOR-001"
        message:str = "No user organization role(s) found"
        description:str = "External error: No user organization role(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "ACC-UOR-002"
        message:str = "User organization roles found"
        description:str = "Requested user organization roles found in database"
        data:list[MaleoAccessUserOrganizationRoleQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-UOR-003"
        message:str = "User organization role found"
        description:str = "Requested user organization role found in database"
        data:MaleoAccessUserOrganizationRoleQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-UOR-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-SYR-005"
        message:str = "Failed creating user organization role"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-SYR-006"
        message:str = "Succesfully created new user organization role"
        description:str = "A new user organization role is created with data provided on request"
        data:MaleoAccessUserOrganizationRoleQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No user organization role(s) found Response",
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