from typing import Union
from maleo_core.clients.maleo_suite.maleo_access.http.controllers.organization_type import MaleoAccessOrganizationTypeHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.organization_type import MaleoAccessOrganizationTypeClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization_type import MaleoAccessOrganizationTypeGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.client.http.services.organization_type import MaleoAccessHTTPClientOrganizationTypeServiceResults

class MaleoAccessOrganizationTypeHTTPService:
    @staticmethod
    async def get_organization_types(
        parameters:MaleoAccessOrganizationTypeClientParameters.Get
    ) -> Union[
        MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationTypeServiceResults.MultipleData
    ]:
        """Fetch organization types from maleo-access"""
        result = await MaleoAccessOrganizationTypeHTTPController.get_organization_types(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_organization_type(
        parameters:MaleoAccessOrganizationTypeGeneralParameters.GetSingle
    ) -> Union[
        MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationTypeServiceResults.SingleData
    ]:
        """Fetch organization type from maleo-access"""
        result = await MaleoAccessOrganizationTypeHTTPController.get_organization_type(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoAccessOrganizationTypeGeneralParameters.CreateOrUpdate) -> Union[
        MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationTypeServiceResults.SingleData
    ]:
        """Create new organization type"""
        result = await MaleoAccessOrganizationTypeHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        organization_type_id:int,
        parameters:MaleoAccessOrganizationTypeGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationTypeServiceResults.SingleData
    ]:
        """Update organization type's data"""
        result = await MaleoAccessOrganizationTypeHTTPController.update(organization_type_id=organization_type_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        organization_type_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationTypeServiceResults.SingleData
    ]:
        """Update organization type's status"""
        result = await MaleoAccessOrganizationTypeHTTPController.status_update(organization_type_id=organization_type_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationTypeServiceResults.SingleData.model_validate(result.content)