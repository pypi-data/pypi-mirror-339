from typing import Union
from maleo_core.clients.maleo_suite.maleo_security.http.controllers.hash.bcrypt import MaleoSecurityBcryptHashHTTPController
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.hash.bcrypt import MaleoSecurityBcryptHashGeneralParameters
from maleo_core.models.maleo_suite.maleo_security.transfers.results.general.hash import MaleoSecurityHashGeneralResults

class MaleoSecurityBcryptHashHTTPService:
    @staticmethod
    async def hash(
        parameters:MaleoSecurityBcryptHashGeneralParameters.Hash
    ) -> Union[
        MaleoSecurityHashGeneralResults.Fail,
        MaleoSecurityHashGeneralResults.Hash
    ]:
        """Hash a message"""
        result = await MaleoSecurityBcryptHashHTTPController.hash(parameters=parameters)
        if not result.success:
            return MaleoSecurityHashGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityHashGeneralResults.Hash.model_validate(result.content)

    @staticmethod
    async def verify(
        parameters:MaleoSecurityBcryptHashGeneralParameters.Verify
    ) -> Union[
        MaleoSecurityHashGeneralResults.Fail,
        MaleoSecurityHashGeneralResults.Verify
    ]:
        """verify a message's hash"""
        result = await MaleoSecurityBcryptHashHTTPController.verify(parameters=parameters)
        if not result.success:
            return MaleoSecurityHashGeneralResults.Fail.model_validate(result.content)
        else:
            return MaleoSecurityHashGeneralResults.Verify.model_validate(result.content)