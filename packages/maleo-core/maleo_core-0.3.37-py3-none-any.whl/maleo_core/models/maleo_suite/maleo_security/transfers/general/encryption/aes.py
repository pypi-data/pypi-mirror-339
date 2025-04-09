from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoSecurityAESEncryptionGeneralTransfers:
    class SinglePlain(BaseModel):
        plaintext:str = Field(..., description="Plaintext")

    class MultiplePlains(BaseModel):
        plaintexts:list[str] = Field(..., description="Plaintexts")

    class BaseCipher(BaseModel):
        aes_key:str = Field(..., description="AES Key")

    class CipherPackage(BaseModel):
        initialization_vector:str = Field(..., description="Initialization Vector")
        ciphertext:str = Field(..., description="Ciphertext")

    class SingleCipher(BaseCipher):
        cipher_package:MaleoSecurityAESEncryptionGeneralTransfers.CipherPackage = Field(..., description="Cipher package")

    class MultipleCiphers(BaseCipher):
        cipher_packages:list[MaleoSecurityAESEncryptionGeneralTransfers.CipherPackage] = Field(..., description="Cipher package")