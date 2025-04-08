from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class BackupDetails(BaseModel):
    """
    Contains the details of the backup created for the table.

    Attributes
    ----------
    BackupArn : str
        ARN associated with the backup. Minimum length of 37. Maximum length of 1024.
    BackupCreationDateTime : datetime
        Time at which the backup was created. This is the request time of the backup.
    BackupName : str
        Name of the requested backup. Minimum length of 3. Maximum length of 255.
        Pattern: [a-zA-Z0-9_.-]+
    BackupStatus : Literal['CREATING', 'DELETED', 'AVAILABLE']
        Backup can be in one of the following states: CREATING, ACTIVE, DELETED.
    BackupType : Literal['USER', 'SYSTEM', 'AWS_BACKUP']
        BackupType:
        USER - You create and manage these using the on-demand backup feature.
        SYSTEM - If you delete a table with point-in-time recovery enabled, a SYSTEM
        backup is automatically created and is retained for 35 days
        (at no additional cost). System backups allow you to restore the
        deleted table to the state it was in just before the point of deletion.
        AWS_BACKUP - On-demand backup created by you from AWS Backup service.
    BackupExpiryDateTime : Optional[datetime]
        Time at which the automatic on-demand backup created by DynamoDB will expire.
        This SYSTEM on-demand backup expires automatically 35 days after its creation.
    BackupSizeBytes : Optional[int]
        Size of the backup in bytes. DynamoDB updates this value approximately every
        six hours. Recent changes might not be reflected in this value.
        Valid Range: Minimum value of 0.
    """

    BackupArn: str = Field(..., min_length=37, max_length=1024)
    BackupCreationDateTime: datetime
    BackupName: str = Field(
        ..., min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+"
    )
    BackupStatus: Literal["CREATING", "DELETED", "AVAILABLE"]
    BackupType: Literal["USER", "SYSTEM", "AWS_BACKUP"]
    BackupExpiryDateTime: datetime | None = None
    BackupSizeBytes: int | None = Field(None, ge=0)
