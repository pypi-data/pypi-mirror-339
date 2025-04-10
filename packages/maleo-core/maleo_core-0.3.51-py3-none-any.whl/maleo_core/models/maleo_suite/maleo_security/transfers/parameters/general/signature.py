from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.maleo_suite.maleo_security.transfers.general.signature import MaleoSecuritySignatureGeneralTransfers

class MaleoSecuritySignatureGeneralParameters:
    class PrivateKey(BaseModel):
        private_key:str = Field(..., description="Private key in str format.")

    class SignSingle(MaleoSecuritySignatureGeneralTransfers.SingleMessage, PrivateKey): pass
    class SignMultiple(MaleoSecuritySignatureGeneralTransfers.MultipleMessages, PrivateKey): pass

    class PublicKey(BaseModel):
        public_key:str = Field(..., description="Public key in str format.")

    class VerifySingle(MaleoSecuritySignatureGeneralTransfers.SingleSignature, PublicKey): pass
    class VerifyMultiple(MaleoSecuritySignatureGeneralTransfers.MultipleSignatures, PublicKey): pass