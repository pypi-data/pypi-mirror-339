from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoSecurityRSAEncryptionGeneralTransfers:
    class SinglePlain(BaseModel):
        plaintext:str = Field(..., description="Plaintext")

    class MultiplePlains(BaseModel):
        plaintexts:list[str] = Field(..., description="Plaintexts")

    class SingleCipher(BaseModel):
        ciphertext:str = Field(..., description="Ciphertext")

    class MultipleCiphers(BaseModel):
        ciphertexts:list[str] = Field(..., description="Ciphertexts")