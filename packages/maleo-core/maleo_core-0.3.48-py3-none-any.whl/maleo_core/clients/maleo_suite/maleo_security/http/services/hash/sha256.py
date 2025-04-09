from typing import Union
from maleo_core.clients.maleo_suite.maleo_security.http.controllers.hash.sha256 import MaleoSecuritySHA256HashHTTPController
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.hash.sha256 import MaleoSecuritySHA256HashGeneralParameters
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.hash import MaleoSecurityHashGeneralResults

class MaleoSecuritySHA256HashHTTPService:
    @staticmethod
    async def hash(
        parameters:MaleoSecuritySHA256HashGeneralParameters.Hash
    ) -> Union[
        MaleoSecurityHashGeneralResults.Fail,
        MaleoSecurityHashGeneralResults.Hash
    ]:
        """Hash a message"""
        result = await MaleoSecuritySHA256HashHTTPController.hash(parameters=parameters)
        if not result.success:
            return MaleoSecurityHashGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityHashGeneralResults.Hash.model_validate(result.content)

    @staticmethod
    async def verify(
        parameters:MaleoSecuritySHA256HashGeneralParameters.Verify
    ) -> Union[
        MaleoSecurityHashGeneralResults.Fail,
        MaleoSecurityHashGeneralResults.Verify
    ]:
        """verify a message's hash"""
        result = await MaleoSecuritySHA256HashHTTPController.verify(parameters=parameters)
        if not result.success:
            return MaleoSecurityHashGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityHashGeneralResults.Verify.model_validate(result.content)