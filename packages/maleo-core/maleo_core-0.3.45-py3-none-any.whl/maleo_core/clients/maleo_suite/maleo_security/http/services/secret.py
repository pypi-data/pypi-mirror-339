from typing import Union
from maleo_core.clients.maleo_suite.maleo_security.http.controllers.secret import MaleoSecuritySecretHTTPController
from maleo_core.models.maleo_suite.maleo_security.transfers.general.secret import MaleoSecuritySecretGeneralTransfers

class MaleoSecuritySecretHTTPService:
    @staticmethod
    async def get(
        parameters:MaleoSecuritySecretGeneralTransfers.GetParameters
    ) -> Union[
        MaleoSecuritySecretGeneralTransfers.Fail,
        MaleoSecuritySecretGeneralTransfers.SingleData
    ]:
        """Fetch secret"""
        result = await MaleoSecuritySecretHTTPController.get(parameters=parameters)
        if not result.success:
            return MaleoSecuritySecretGeneralTransfers.Fail.model_validate(result.content)
        else:
            return MaleoSecuritySecretGeneralTransfers.SingleData.model_validate(result.content)

    @staticmethod
    async def create(parameters:MaleoSecuritySecretGeneralTransfers.CreateParameters) -> Union[
        MaleoSecuritySecretGeneralTransfers.Fail,
        MaleoSecuritySecretGeneralTransfers.SingleData
    ]:
        """Create new secret"""
        result = await MaleoSecuritySecretHTTPController.create(parameters=parameters)
        if not result.success:
            return MaleoSecuritySecretGeneralTransfers.Fail.model_validate(result.content)
        else:
            return MaleoSecuritySecretGeneralTransfers.SingleData.model_validate(result.content)