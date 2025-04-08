from typing import Union
from maleo_core.clients.maleo_suite.maleo_access.http.controllers.organization_role import MaleoAccessOrganizationRoleHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.organization_role import MaleoAccessOrganizationRoleClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization_role import MaleoAccessOrganizationRoleGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.client.http.services.organization_role import MaleoAccessHTTPClientOrganizationRoleServiceResults

class MaleoAccessOrganizationRoleHTTPService:
    @staticmethod
    async def get_organization_roles(
        parameters:MaleoAccessOrganizationRoleClientParameters.Get
    ) -> Union[
        MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationRoleServiceResults.MultipleData
    ]:
        """Fetch organization roles from maleo-access"""
        result = await MaleoAccessOrganizationRoleHTTPController.get_organization_roles(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_organization_role(
        parameters:MaleoAccessOrganizationRoleGeneralParameters.GetSingle
    ) -> Union[
        MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationRoleServiceResults.SingleData
    ]:
        """Fetch organization role from maleo-access"""
        result = await MaleoAccessOrganizationRoleHTTPController.get_organization_role(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoAccessOrganizationRoleGeneralParameters.CreateOrUpdate) -> Union[
        MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationRoleServiceResults.SingleData
    ]:
        """Create new organization role"""
        result = await MaleoAccessOrganizationRoleHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        organization_role_id:int,
        parameters:MaleoAccessOrganizationRoleGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationRoleServiceResults.SingleData
    ]:
        """Update organization role's data"""
        result = await MaleoAccessOrganizationRoleHTTPController.update(organization_role_id=organization_role_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        organization_role_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail,
        MaleoAccessHTTPClientOrganizationRoleServiceResults.SingleData
    ]:
        """Update organization role's status"""
        result = await MaleoAccessOrganizationRoleHTTPController.status_update(organization_role_id=organization_role_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientOrganizationRoleServiceResults.SingleData.model_validate(result.content)