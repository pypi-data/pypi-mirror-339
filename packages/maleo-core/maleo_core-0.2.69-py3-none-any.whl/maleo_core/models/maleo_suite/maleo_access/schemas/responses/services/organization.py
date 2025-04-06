from __future__ import annotations
from fastapi import status
from pydantic import field_serializer, FieldSerializationInfo
from typing import Any
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization import MaleoAccessOrganizationGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.organization import MaleoAccessOrganizationQueryResults

class MaleoAccessOrganizationServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-ORG-001"
        message:str = "No organization(s) found"
        description:str = "External error: No organization(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "ACC-ORG-002"
        message:str = "Organizations found"
        description:str = "Requested organizations found in database"
        data:list[MaleoAccessOrganizationQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-ORG-003"
        message:str = "Organization found"
        description:str = "Requested organization found in database"
        data:MaleoAccessOrganizationQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-ORG-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-ORG-005"
        message:str = "Failed creating organization"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-ORG-006"
        message:str = "Succesfully created new organization"
        description:str = "A new organization is created with data provided on request"
        data:MaleoAccessOrganizationQueryResults.Get

    class UpdateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-ORG-007"
        message:str = "Failed updating organization"

    class UpdateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-ORG-008"
        message:str = "Succesfully updated organization"
        data:MaleoAccessOrganizationQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No organization(s) found Response",
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