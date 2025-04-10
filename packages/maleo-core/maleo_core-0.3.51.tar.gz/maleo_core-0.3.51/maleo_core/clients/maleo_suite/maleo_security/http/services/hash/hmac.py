from typing import Union
from maleo_core.clients.maleo_suite.maleo_security.http.controllers.hash.hmac import MaleoSecurityHMACHashHTTPController
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.hash.hmac import MaleoSecurityHMACHashGeneralParameters
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.hash import MaleoSecurityHashGeneralResults

class MaleoSecurityHMACHashHTTPService:
    @staticmethod
    async def hash(
        parameters:MaleoSecurityHMACHashGeneralParameters.Hash
    ) -> Union[
        MaleoSecurityHashGeneralResults.Fail,
        MaleoSecurityHashGeneralResults.Hash
    ]:
        """Hash a message"""
        result = await MaleoSecurityHMACHashHTTPController.hash(parameters=parameters)
        if not result.success:
            return MaleoSecurityHashGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityHashGeneralResults.Hash.model_validate(result.content)

    @staticmethod
    async def verify(
        parameters:MaleoSecurityHMACHashGeneralParameters.Verify
    ) -> Union[
        MaleoSecurityHashGeneralResults.Fail,
        MaleoSecurityHashGeneralResults.Verify
    ]:
        """verify a message's hash"""
        result = await MaleoSecurityHMACHashHTTPController.verify(parameters=parameters)
        if not result.success:
            return MaleoSecurityHashGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityHashGeneralResults.Verify.model_validate(result.content)