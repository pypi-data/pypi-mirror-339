from typing import Union
from maleo_core.clients.maleo_suite.maleo_access.http.controllers.system_role import MaleoAccessSystemRoleHTTPController
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.system_role import MaleoAccessSystemRoleClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.system_role import MaleoAccessSystemRoleGeneralParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.results.client.http.services.system_role import MaleoAccessHTTPClientSystemRoleServiceResults

class MaleoAccessSystemRoleHTTPService:
    @staticmethod
    async def get_system_roles(
        parameters:MaleoAccessSystemRoleClientParameters.Get
    ) -> Union[
        MaleoAccessHTTPClientSystemRoleServiceResults.Fail,
        MaleoAccessHTTPClientSystemRoleServiceResults.MultipleData
    ]:
        """Fetch system roles from maleo-access"""
        result = await MaleoAccessSystemRoleHTTPController.get_system_roles(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientSystemRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientSystemRoleServiceResults.MultipleData.model_validate(result.content)

    @staticmethod
    async def get_system_role(
        parameters:MaleoAccessSystemRoleGeneralParameters.GetSingle
    ) -> Union[
        MaleoAccessHTTPClientSystemRoleServiceResults.Fail,
        MaleoAccessHTTPClientSystemRoleServiceResults.SingleData
    ]:
        """Fetch system role from maleo-access"""
        result = await MaleoAccessSystemRoleHTTPController.get_system_role(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientSystemRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientSystemRoleServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoAccessSystemRoleGeneralParameters.CreateOrUpdate) -> Union[
        MaleoAccessHTTPClientSystemRoleServiceResults.Fail,
        MaleoAccessHTTPClientSystemRoleServiceResults.SingleData
    ]:
        """Create new system role"""
        result = await MaleoAccessSystemRoleHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientSystemRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientSystemRoleServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def update(
        system_role_id:int,
        parameters:MaleoAccessSystemRoleGeneralParameters.CreateOrUpdate
    ) -> Union[
        MaleoAccessHTTPClientSystemRoleServiceResults.Fail,
        MaleoAccessHTTPClientSystemRoleServiceResults.SingleData
    ]:
        """Update system role's data"""
        result = await MaleoAccessSystemRoleHTTPController.update(system_role_id=system_role_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientSystemRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientSystemRoleServiceResults.SingleData.model_validate(result.content)

    @staticmethod
    async def status_update(
        system_role_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> Union[
        MaleoAccessHTTPClientSystemRoleServiceResults.Fail,
        MaleoAccessHTTPClientSystemRoleServiceResults.SingleData
    ]:
        """Update system role's status"""
        result = await MaleoAccessSystemRoleHTTPController.status_update(system_role_id=system_role_id, parameters=parameters)
        if not result.success:
            return MaleoAccessHTTPClientSystemRoleServiceResults.Fail.model_validate(result.content)
        else:
            return MaleoAccessHTTPClientSystemRoleServiceResults.SingleData.model_validate(result.content)