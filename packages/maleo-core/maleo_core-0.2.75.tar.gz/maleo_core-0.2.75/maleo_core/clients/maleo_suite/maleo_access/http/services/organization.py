from typing import Union
from maleo_core.clients.maleo_suite.maleo_access.http.controllers.organization import MaleoAccessOrganizationHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.organization import MaleoAccessOrganizationClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization import MaleoAccessOrganizationGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.client.http.services.organization import MaleoAccessHTTPClientOrganizationServiceResults

class MaleoAccessOrganizationHTTPService:
    @staticmethod
    async def get_organizations(
        parameters:MaleoAccessOrganizationClientParameters.Get
    ) -> Union[
        MaleoAccessHTTPClientOrganizationServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationServiceResults.MultipleData
    ]:
        """Fetch organizations from maleo-access"""
        result = await MaleoAccessOrganizationHTTPController.get_organizations(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_organization(
        parameters:MaleoAccessOrganizationGeneralParameters.GetSingle
    ) -> Union[
        MaleoAccessHTTPClientOrganizationServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationServiceResults.SingleData
    ]:
        """Fetch organization from maleo-access"""
        result = await MaleoAccessOrganizationHTTPController.get_organization(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoAccessOrganizationGeneralParameters.CreateOrUpdate) -> Union[
        MaleoAccessHTTPClientOrganizationServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationServiceResults.SingleData
    ]:
        """Create new organization"""
        result = await MaleoAccessOrganizationHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        organization_id:int,
        parameters:MaleoAccessOrganizationGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoAccessHTTPClientOrganizationServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationServiceResults.SingleData
    ]:
        """Update organization's data"""
        result = await MaleoAccessOrganizationHTTPController.update(organization_id=organization_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        organization_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoAccessHTTPClientOrganizationServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationServiceResults.SingleData
    ]:
        """Update organization's status"""
        result = await MaleoAccessOrganizationHTTPController.status_update(organization_id=organization_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationServiceResults.SingleData.model_validate(result.content)