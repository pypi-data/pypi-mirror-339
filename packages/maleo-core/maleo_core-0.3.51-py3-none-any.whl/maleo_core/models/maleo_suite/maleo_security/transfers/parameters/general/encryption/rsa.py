from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.maleo_suite.maleo_security.transfers.general.encryption.rsa import MaleoSecurityRSAEncryptionGeneralTransfers

class MaleoSecurityRSAEncryptionGeneralParameters:
    class PublicKey(BaseModel):
        public_key:str = Field(..., description="Public key in str format.")

    class EncryptSingle(MaleoSecurityRSAEncryptionGeneralTransfers.SinglePlain, PublicKey): pass
    class EncryptMultiple(MaleoSecurityRSAEncryptionGeneralTransfers.MultiplePlains, PublicKey): pass

    class PrivateKey(BaseModel):
        private_key:str = Field(..., description="Private key in str format.")

    class DecryptSingle(MaleoSecurityRSAEncryptionGeneralTransfers.SingleCipher, PrivateKey): pass
    class DecryptMultiple(MaleoSecurityRSAEncryptionGeneralTransfers.MultipleCiphers, PrivateKey): pass