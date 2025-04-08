# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class BackupSummary(BaseModel):
    """
    Contains details for the backup.

    Attributes
    ----------
    BackupArn : Optional[str]
        ARN associated with the backup. Minimum length of 37. Maximum length of 1024.
    BackupCreationDateTime : Optional[datetime]
        Time at which the backup was created.
    BackupExpiryDateTime : Optional[datetime]
        Time at which the automatic on-demand backup created by DynamoDB will expire.
        This SYSTEM on-demand backup expires automatically 35 days after its creation.
    BackupName : Optional[str]
        Name of the specified backup. Minimum length of 3. Maximum length of 255.
        Pattern: [a-zA-Z0-9_.-]+
    BackupSizeBytes : Optional[int]
        Size of the backup in bytes. Valid Range: Minimum value of 0.
    BackupStatus : Optional[Literal['CREATING', 'DELETED', 'AVAILABLE']]
        Backup can be in one of the following states: CREATING, ACTIVE, DELETED.
    BackupType : Optional[Literal['USER', 'SYSTEM', 'AWS_BACKUP']]
        BackupType:
        USER - You create and manage these using the on-demand backup feature.
        SYSTEM - If you delete a table with point-in-time recovery enabled, a SYSTEM
        backup is automatically created and is retained for 35 days
        (at no additional cost). System backups allow you to restore the deleted
        table to the state it was in just before the point of deletion.
        AWS_BACKUP - On-demand backup created by you from AWS Backup service.
    TableArn : Optional[str]
        ARN associated with the table. Minimum length of 1. Maximum length of 1024.
    TableId : Optional[str]
        Unique identifier for the table. Pattern: [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}
    TableName : Optional[str]
        Name of the table. Minimum length of 3. Maximum length of 255.
        Pattern: [a-zA-Z0-9_.-]+
    """

    BackupArn: str | None = Field(None, min_length=37, max_length=1024)
    BackupCreationDateTime: datetime | None = None
    BackupExpiryDateTime: datetime | None = None
    BackupName: str | None = Field(
        None, min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+"
    )
    BackupSizeBytes: int | None = Field(None, ge=0)
    BackupStatus: Literal["CREATING", "DELETED", "AVAILABLE"] | None = None
    BackupType: Literal["USER", "SYSTEM", "AWS_BACKUP"] | None = None
    TableArn: str | None = Field(None, min_length=1, max_length=1024)
    TableId: str | None = Field(
        None, pattern=r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    )
    TableName: str | None = Field(
        None, min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+"
    )
