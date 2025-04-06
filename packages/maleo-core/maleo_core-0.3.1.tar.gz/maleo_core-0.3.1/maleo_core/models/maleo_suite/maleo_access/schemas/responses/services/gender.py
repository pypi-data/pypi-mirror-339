from fastapi import status
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.schemas.responses.service import BaseServiceResponsesSchemas
from maleo_core.models.maleo_suite.maleo_access.transfers.results.query.gender import MaleoAccessGenderQueryResults

class MaleoAccessGenderServiceResponsesSchemas:
    #* ----- ----- Response ----- ----- *#
    class NotFoundResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-GND-001"
        message:str = "No gender(s) found"
        description:str = "External error: No gender(s) found in database acording to given parameter(s)"
        other:str = "Ensure parameter(s) are correct"

    class GetMultipleResponse(BaseServiceResponsesSchemas.MultipleData):
        code:str = "ACC-GND-002"
        message:str = "Genders found"
        description:str = "Requested genders found in database"
        data:list[MaleoAccessGenderQueryResults.Get]

    class GetSingleResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-GND-003"
        message:str = "Gender found"
        description:str = "Requested gender found in database"
        data:MaleoAccessGenderQueryResults.Get

    class StatusUpdateResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-GND-004"

    class CreateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-GND-005"
        message:str = "Failed creating gender"

    class CreateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-GND-006"
        message:str = "Succesfully created new gender"
        description:str = "A new gender is created with data provided on request"
        data:MaleoAccessGenderQueryResults.Get

    class UpdateFailedResponse(BaseGeneralResponsesSchemas.Fail):
        code:str = "ACC-GND-007"
        message:str = "Failed updating gender"

    class UpdateSuccessResponse(BaseGeneralResponsesSchemas.SingleData):
        code:str = "ACC-GND-008"
        message:str = "Succesfully updated gender"
        data:MaleoAccessGenderQueryResults.Get

    #* ----- ----- Responses Class ----- ----- *#
    not_found_responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "No gender(s) found Response",
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