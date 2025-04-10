from __future__ import annotations
from maleo_core.models.base.transfers.results.general import BaseGeneralResults
from maleo_core.models.maleo_suite.maleo_security.transfers.general.encryption.rsa import MaleoSecurityRSAEncryptionGeneralTransfers

class MaleoSecurityRSAEncryptionGeneralResults:
    EncryptSingle = MaleoSecurityRSAEncryptionGeneralTransfers.SingleCipher
    EncryptMultiple = MaleoSecurityRSAEncryptionGeneralTransfers.MultipleCiphers
    DecryptSingle = MaleoSecurityRSAEncryptionGeneralTransfers.SinglePlain
    DecryptMultiple = MaleoSecurityRSAEncryptionGeneralTransfers.MultiplePlains

    Fail = BaseGeneralResults.Fail

    class SingleEncryption(BaseGeneralResults.SingleData):
        data:MaleoSecurityRSAEncryptionGeneralResults.EncryptSingle

    class MultipleEncryption(BaseGeneralResults.SingleData):
        data:MaleoSecurityRSAEncryptionGeneralResults.EncryptMultiple

    class SingleDecryption(BaseGeneralResults.SingleData):
        data:MaleoSecurityRSAEncryptionGeneralResults.DecryptSingle

    class MultipleDecryption(BaseGeneralResults.SingleData):
        data:MaleoSecurityRSAEncryptionGeneralResults.DecryptMultiple