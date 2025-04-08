from datetime import datetime
from typing import Literal

from pydantic import BaseModel, conint, constr

from .data_types.backup_summary import BackupSummary


class ListBackupsRequest(BaseModel):
    """
    Request model for the ListBackups operation.

    Attributes
    ----------
    TableName : Optional[str]
        Lists the backups from the table specified in TableName.
    Limit : Optional[int]
        Maximum number of backups to return at once.
    TimeRangeLowerBound : Optional[datetime]
        Only backups created after this time are listed.
    TimeRangeUpperBound : Optional[datetime]
        Only backups created before this time are listed.
    BackupType : Optional[Literal['USER', 'SYSTEM', 'AWS_BACKUP', 'ALL']]
        The backups from the table specified by BackupType are listed.
    ExclusiveStartBackupArn : Optional[str]
        The ARN of the backup last evaluated when the current page of results
        was returned.
    """

    TableName: constr(min_length=1, max_length=1024) | None = None
    Limit: conint(ge=1, le=100) | None = None
    TimeRangeLowerBound: datetime | None = None
    TimeRangeUpperBound: datetime | None = None
    BackupType: Literal["USER", "SYSTEM", "AWS_BACKUP", "ALL"] | None = None
    ExclusiveStartBackupArn: constr(min_length=37, max_length=1024) | None = None


class ListBackupsResponse(BaseModel):
    """
    Response model for the ListBackups operation.

    Attributes
    ----------
    BackupSummaries : Optional[List[BackupSummary]]
        List of backup summaries.
    LastEvaluatedBackupArn : Optional[str]
        The ARN of the backup last evaluated when the current page of results was
        returned.
    """

    BackupSummaries: list[BackupSummary] | None = None
    LastEvaluatedBackupArn: constr(min_length=37, max_length=1024) | None = None
