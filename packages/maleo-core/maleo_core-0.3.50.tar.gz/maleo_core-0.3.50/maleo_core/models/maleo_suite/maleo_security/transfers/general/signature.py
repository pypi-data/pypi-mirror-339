from __future__ import annotations
from pydantic import BaseModel, Field

class MaleoSecuritySignatureGeneralTransfers:
    class SingleMessage(BaseModel):
        message:str = Field(..., description="Message to be signed")

    class MultipleMessages(BaseModel):
        messages:list[str] = Field(..., description="Messages to be signed")

    class Signature(BaseModel):
        signature:str = Field(..., description="Signature value")

    class SignaturePackage(Signature, SingleMessage): pass

    class SingleSignature(BaseModel):
        signature_package:MaleoSecuritySignatureGeneralTransfers.SignaturePackage = Field(..., description="Signature package")

    class MultipleSignatures(BaseModel):
        signature_packages:list[MaleoSecuritySignatureGeneralTransfers.SignaturePackage] = Field(..., description="Signature packages")