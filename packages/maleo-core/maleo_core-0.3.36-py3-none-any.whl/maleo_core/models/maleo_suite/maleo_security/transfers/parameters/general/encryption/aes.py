from __future__ import annotations
from maleo_core.models.maleo_suite.maleo_security.transfers.general.encryption.aes import MaleoSecurityAESEncryptionGeneralTransfers

class MaleoSecurityAESEncryptionGeneralParameters:
    EncryptSingle = MaleoSecurityAESEncryptionGeneralTransfers.BasePlain
    EncryptMultiple = list[MaleoSecurityAESEncryptionGeneralTransfers.BasePlain]
    DecryptSingle = MaleoSecurityAESEncryptionGeneralTransfers.BaseSingleCipher
    DecryptMultiple = MaleoSecurityAESEncryptionGeneralTransfers.BaseMultipleCiphers