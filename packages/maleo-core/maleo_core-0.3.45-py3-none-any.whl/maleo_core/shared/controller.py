from fastapi import status
from typing import Callable, Type, Union, Any
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.services.general import BaseServiceGeneralResults
from maleo_core.models.base.transfers.results.services.controllers.rest import BaseServiceRESTControllerResults

class BaseController:
    @staticmethod
    def check_unique_existence(
        check:BaseGeneralParameters.UniqueFieldCheck,
        get_single_parameters_class:Type[BaseGeneralParameters.GetSingle],
        get_single_service_function:Callable[[BaseGeneralParameters.GetSingle], Union[BaseServiceGeneralResults.Fail, BaseServiceGeneralResults.SingleData]],
        create_failed_response_class:Type[BaseGeneralResponsesSchemas.Fail],
        update_failed_response_class:Type[BaseGeneralResponsesSchemas.Fail],
        **additional_get_parameters:Any
    ) -> BaseServiceRESTControllerResults:
        """Generic helper function to check if a unique value exists in the database."""

        #* Return early if nullable and no new value
        if check.nullable and check.new_value is None:
            return BaseServiceRESTControllerResults(success=True, content=None)

        #* Return early if values are unchanged on update
        if check.operation == BaseGeneralParameters.OperationType.UPDATE and check.old_value == check.new_value:
            return BaseServiceRESTControllerResults(success=True, content=None)

        #* Prepare parameters to query for existing data
        get_single_parameters = get_single_parameters_class(identifier=check.field, value=check.new_value)

        #* Query the existing data using provided function
        service_result:Union[BaseServiceGeneralResults.Fail, BaseServiceGeneralResults.SingleData] = get_single_service_function(parameters=get_single_parameters, **additional_get_parameters)
        if not service_result.success:
            content = BaseGeneralResponsesSchemas.ServerError.model_validate(service_result.model_dump(exclude_unset=True)).model_dump()
            return BaseServiceRESTControllerResults(success=False, content=content, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #* Handle case if duplicate is found
        if service_result.data:
            description = f"External error: {check.field} of '{check.new_value}' already exists in the database"
            other = check.suggestion or f"Select another {check.field} value"
            if check.operation == BaseGeneralParameters.OperationType.CREATE:
                content = create_failed_response_class(description=description, other=other).model_dump()
            elif check.operation == BaseGeneralParameters.OperationType.UPDATE:
                content = update_failed_response_class(description=description, other=other).model_dump()

            return BaseServiceRESTControllerResults(success=False, content=content, status_code=status.HTTP_400_BAD_REQUEST)

        #* No duplicates found
        return BaseServiceRESTControllerResults(success=True, content=None)