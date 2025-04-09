from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoSecurityAESEncryptionGeneralTransfers:
    class BasePlain(BaseModel):
        plaintext:str = Field(..., description="Plaintext")

    class BaseCipher(BaseModel):
        aes_key:str = Field(..., description="AES Key")

    class CipherPackage(BaseModel):
        initialization_vector:str = Field(..., description="Initialization Vector")
        ciphertext:str = Field(..., description="Ciphertext")

    class BaseSingleCipher(BaseCipher):
        cipher_package:MaleoSecurityAESEncryptionGeneralTransfers.CipherPackage = Field(..., description="Cipher package")

    class BaseMultipleCiphers(BaseCipher):
        cipher_packages:list[MaleoSecurityAESEncryptionGeneralTransfers.CipherPackage] = Field(..., description="Cipher package")