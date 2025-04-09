from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_core.models.maleo_suite.maleo_security.transfers.general.encryption.rsa import MaleoSecurityRSAEncryptionGeneralTransfers

class MaleoSecurityRSAEncryptionGeneralParameters:
    class PublicKey(BaseModel):
        public_key:str = Field(..., description="Public key in str format.")

    class EncryptSingle(PublicKey, MaleoSecurityRSAEncryptionGeneralTransfers.SinglePlain): pass
    class EncryptMultiple(PublicKey, MaleoSecurityRSAEncryptionGeneralTransfers.MultiplePlains): pass
    
    class PrivateKey(BaseModel):
        private_key:str = Field(..., description="Private key in str format.")
    
    class DecryptSingle(PrivateKey, MaleoSecurityRSAEncryptionGeneralTransfers.SingleCipher): pass
    class DecryptMultiple(PrivateKey, MaleoSecurityRSAEncryptionGeneralTransfers.MultipleCiphers): pass