from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class SSEDescription(BaseModel):
    """
    The description of the server-side encryption status on the specified table.

    Attributes
    ----------
    InaccessibleEncryptionDateTime : Optional[datetime]
        Indicates the time, in UNIX epoch date format, when DynamoDB detected that the
        table's AWS KMS key was inaccessible.
    KMSMasterKeyArn : Optional[str]
        The AWS KMS key ARN used for the AWS KMS encryption.
    SSEType : Optional[Literal['AES256', 'KMS']]
        Server-side encryption type.
    Status : Optional[Literal['ENABLING', 'ENABLED', 'DISABLING', 'DISABLED',
    'UPDATING']]
        Represents the current state of server-side encryption.
    """

    InaccessibleEncryptionDateTime: datetime | None = None
    KMSMasterKeyArn: str | None = None
    SSEType: Literal["AES256", "KMS"] | None = None
    Status: (
        Literal["ENABLING", "ENABLED", "DISABLING", "DISABLED", "UPDATING"] | None
    ) = None  # noqa: E501
