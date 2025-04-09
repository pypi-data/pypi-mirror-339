from __future__ import annotations
from maleo_core.models.maleo_suite.maleo_security.transfers.general.encryption.aes import MaleoSecurityAESEncryptionGeneralTransfers

class MaleoSecurityAESEncryptionGeneralParameters:
    EncryptSingle = MaleoSecurityAESEncryptionGeneralTransfers.SinglePlain
    EncryptMultiple = MaleoSecurityAESEncryptionGeneralTransfers.MultiplePlains
    DecryptSingle = MaleoSecurityAESEncryptionGeneralTransfers.SingleCipher
    DecryptMultiple = MaleoSecurityAESEncryptionGeneralTransfers.MultipleCiphers