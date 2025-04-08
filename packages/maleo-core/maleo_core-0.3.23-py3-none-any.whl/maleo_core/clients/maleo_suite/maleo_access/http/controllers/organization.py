from maleo_core.clients.maleo_suite.maleo_access.http.manager import MaleoAccessHTTPClientManager
from maleo_core.models.base.transfers.parameters.general import BaseGeneralParameters
from maleo_core.models.base.transfers.results.clients.http.controller import BaseHTTPClientControllerResults
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.client.organization import MaleoAccessOrganizationClientParameters
from maleo_core.models.maleo_suite.maleo_access.transfers.parameters.general.organization import MaleoAccessOrganizationGeneralParameters

class MaleoAccessOrganizationHTTPController:
    @staticmethod
    async def get_organizations(
        parameters:MaleoAccessOrganizationClientParameters.Get
    ) -> BaseHTTPClientControllerResults:
        """Fetch organizations from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organizations/"

            query_parameters = MaleoAccessOrganizationClientParameters.GetQuery.model_validate(parameters.model_dump())
            params = query_parameters.to_query_params()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def get_organization(
        parameters:MaleoAccessOrganizationGeneralParameters.GetSingle
    ) -> BaseHTTPClientControllerResults:
        """Fetch organization from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organizations/"
            if parameters.identifier == MaleoAccessOrganizationGeneralParameters.UniqueIdentifiers.ID:
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
    async def get_organization_childrens(
        organization_id:int,
        parameters:MaleoAccessOrganizationClientParameters.GetChildren
    ) -> BaseHTTPClientControllerResults:
        """Fetch organization's childrens from maleo-access"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organizations/{organization_id}/childrens"

            #* Construct query parameters
            query_params = MaleoAccessOrganizationClientParameters.GetChildrenQuery.model_validate(parameters.model_dump())
            params = query_params.model_dump()

            #* Get Response
            response = await client.get(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def create(parameters:MaleoAccessOrganizationGeneralParameters.CreateOrUpdate) -> BaseHTTPClientControllerResults:
        """Create new organization"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organizations/"

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
        organization_id:int,
        parameters:MaleoAccessOrganizationGeneralParameters.CreateOrUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update organization's data"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organizations/{organization_id}"

            #* Define headers
            headers = {
                "Content-": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.put(url=url, json=json, headers=headers)
            return BaseHTTPClientControllerResults(response=response)

    @staticmethod
    async def status_update(
        organization_id:int,
        parameters:MaleoAccessOrganizationGeneralParameters.StatusUpdate
    ) -> BaseHTTPClientControllerResults:
        """Update organization's status"""
        async with MaleoAccessHTTPClientManager.get() as client:
            #* Define URL
            url = f"{MaleoAccessHTTPClientManager._base_url}/v1/organizations/{organization_id}/status"

            #* Construct query parameters
            params = parameters.model_dump() if parameters else {}

            #* Get Response
            response = await client.patch(url=url, params=params)
            return BaseHTTPClientControllerResults(response=response)