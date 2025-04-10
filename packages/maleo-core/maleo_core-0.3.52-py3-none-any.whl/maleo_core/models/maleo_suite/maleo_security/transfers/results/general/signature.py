from __future__ import annotations
from pydantic import Field
from maleo_core.models.base.transfers.results.general import BaseGeneralResults
from maleo_core.models.maleo_suite.maleo_security.transfers.general.signature import MaleoSecuritySignatureGeneralTransfers
from maleo_core.models.maleo_suite.maleo_security.transfers.parameters.general.signature import MaleoSecuritySignatureGeneralParameters

class MaleoSecuritySignatureGeneralResults:
    class Base(MaleoSecuritySignatureGeneralTransfers.SignaturePackage):
        is_valid:bool = Field(..., description="Whether hash is valid")

    Fail = BaseGeneralResults.Fail

    class SingleSign(BaseGeneralResults.SingleData):
        data:MaleoSecuritySignatureGeneralTransfers.SignaturePackage

    class MultipleSign(BaseGeneralResults.SingleData):
        data:list[MaleoSecuritySignatureGeneralTransfers.SignaturePackage]

    class SingleVerify(BaseGeneralResults.SingleData):
        data:MaleoSecuritySignatureGeneralResults.Base

    class MultipleVerify(BaseGeneralResults.SingleData):
        data:list[MaleoSecuritySignatureGeneralResults.Base]