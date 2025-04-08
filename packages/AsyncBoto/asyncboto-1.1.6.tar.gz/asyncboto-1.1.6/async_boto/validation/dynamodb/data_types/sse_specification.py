from typing import Literal

from pydantic import BaseModel


class SSESpecification(BaseModel):
    """
    Represents the settings used to enable server-side encryption.

    Attributes
    ----------
    Enabled : Optional[bool]
        Indicates whether server-side encryption is done using an AWS managed key
        or an AWS owned key.
    KMSMasterKeyId : Optional[str]
        The AWS KMS key that should be used for the AWS KMS encryption.
    SSEType : Optional[Literal['AES256', 'KMS']]
        Server-side encryption type.
    """

    Enabled: bool | None = None
    KMSMasterKeyId: str | None = None
    SSEType: Literal["AES256", "KMS"] | None = None
