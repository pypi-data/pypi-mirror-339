from typing import Union
from maleo_core.clients.maleo_suite.maleo_security.http.controllers.key import MaleoSecurityKeyHTTPController
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.key import MaleoSecurityKeyGeneralParameters
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.key import MaleoSecurityKeyGeneralResults

class MaleoSecurityKeyHTTPService:
    @staticmethod
    async def generate_private(
        parameters:MaleoSecurityKeyGeneralParameters.GeneratePairOrPrivate
    ) -> Union[
        MaleoSecurityKeyGeneralResults.Fail,
        MaleoSecurityKeyGeneralResults.SinglePrivate
    ]:
        """Generate private key"""
        result = await MaleoSecurityKeyHTTPController.generate_private(parameters=parameters)
        if not result.success:
            return MaleoSecurityKeyGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityKeyGeneralResults.SinglePrivate.model_validate(result.content)

    @staticmethod
    async def generate_public(
        parameters:MaleoSecurityKeyGeneralParameters.GeneratePublic
    ) -> Union[
        MaleoSecurityKeyGeneralResults.Fail,
        MaleoSecurityKeyGeneralResults.SinglePublic
    ]:
        """Generate public key"""
        result = await MaleoSecurityKeyHTTPController.generate_public(parameters=parameters)
        if not result.success:
            return MaleoSecurityKeyGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityKeyGeneralResults.SinglePublic.model_validate(result.content)

    @staticmethod
    async def generate_pair(
        parameters:MaleoSecurityKeyGeneralParameters.GeneratePairOrPrivate
    ) -> Union[
        MaleoSecurityKeyGeneralResults.Fail,
        MaleoSecurityKeyGeneralResults.SinglePair
    ]:
        """Generate key pair"""
        result = await MaleoSecurityKeyHTTPController.generate_pair(parameters=parameters)
        if not result.success:
            return MaleoSecurityKeyGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityKeyGeneralResults.SinglePair.model_validate(result.content)