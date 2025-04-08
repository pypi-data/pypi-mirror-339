from datetime import datetime

from pydantic import BaseModel, constr


class RestoreSummary(BaseModel):
    """
    Contains details for the restore.

    Attributes
    ----------
    RestoreDateTime : datetime
        Point in time or source backup time.
    RestoreInProgress : bool
        Indicates if a restore is in progress or not.
    SourceBackupArn : Optional[str]
        The Amazon Resource Name (ARN) of the backup from which the table was restored.
    SourceTableArn : Optional[str]
        The ARN of the source table of the backup that is being restored.
    """

    RestoreDateTime: datetime
    RestoreInProgress: bool
    SourceBackupArn: constr(min_length=37, max_length=1024) | None = None
    SourceTableArn: constr(min_length=1, max_length=1024) | None = None
