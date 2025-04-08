from maleo_core.clients.maleo_suite.maleo_access.http.manager import MaleoAccessHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.organization_role import MaleoAccessOrganizationRoleClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization_role import MaleoAccessOrganizationRoleGeneralParameters

class MaleoAccessOrganizationRoleHTTPController:
    @staticmethod
    async def get_organization_roles(
        parameters:MaleoAccessOrganizationRoleClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch organization roles from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organization-roles/"

            query_parameters = MaleoAccessOrganizationRoleClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_organization_role(
        parameters:MaleoAccessOrganizationRoleGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch organization role from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organization-roles/"
            if parameters.identifier == MaleoAccessOrganizationRoleGeneralParameters.UniqueIdentifiers.ID:
                url += f"{parameters.value}"
            else:
                url += f"{parameters.identifier.value}/{parameters.value}"

            #* Construct query parameters
            query_params = BaseGeneralParameters.GetSingleQuery.model_validate(parameters.model_dump())
            params = query_params.model_dump()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def create(parameters:MaleoAccessOrganizationRoleGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
        """Create new organization role"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organization-roles/"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def update(
        organization_role_id:int,
        parameters:MaleoAccessOrganizationRoleGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update organization role's data"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organization-roles/{organization_role_id}"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.put(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def status_update(
        organization_role_id:int,
        parameters:BaseGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update organization role's status"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organization-roles/{organization_role_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)