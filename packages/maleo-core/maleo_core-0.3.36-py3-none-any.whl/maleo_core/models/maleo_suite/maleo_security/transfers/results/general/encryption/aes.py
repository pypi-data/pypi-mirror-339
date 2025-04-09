from __future__ import annotations
from maleo_core.models.base.transfers.results.general import BaseGeneralResults
from maleo_core.models.maleo_suite.maleo_security.transfers.general.encryption.aes import MaleoSecurityAESEncryptionGeneralTransfers

class MaleoSecurityAESEncryptionGeneralResults:
    EncryptSingle = MaleoSecurityAESEncryptionGeneralTransfers.BaseSingleCipher
    EncryptMultiple = MaleoSecurityAESEncryptionGeneralTransfers.BaseMultipleCiphers
    DecryptSingle = MaleoSecurityAESEncryptionGeneralTransfers.BasePlain
    DecryptMultiple = list[MaleoSecurityAESEncryptionGeneralTransfers.BasePlain]

    Fail = BaseGeneralResults.Fail

    class SingleEncryption(BaseGeneralResults.SingleData):
        data:MaleoSecurityAESEncryptionGeneralResults.EncryptSingle

    class MultipleEncryption(BaseGeneralResults.SingleData):
        data:MaleoSecurityAESEncryptionGeneralResults.EncryptMultiple

    class SingleDecryption(BaseGeneralResults.SingleData):
        data:MaleoSecurityAESEncryptionGeneralResults.DecryptSingle

    class MultipleDecryption(BaseGeneralResults.SingleData):
        data:MaleoSecurityAESEncryptionGeneralResults.DecryptMultiple