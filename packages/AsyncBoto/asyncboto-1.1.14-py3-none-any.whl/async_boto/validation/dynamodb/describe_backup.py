from pydantic import BaseModel, constr

from .data_types.backup_description import BackupDescription as BackupDescriptionModel


class DescribeBackupRequest(BaseModel):
    """
    Describes an existing backup of a table.

    Attributes
    ----------
    BackupArn : str
        The Amazon Resource Name (ARN) associated with the backup.
    """

    BackupArn: constr(min_length=37, max_length=1024)


class DescribeBackupResponse(BaseModel):
    """
    Response for the DescribeBackup operation.

    Attributes
    ----------
    BackupDescription : BackupDescription
        Contains the description of the backup.
    """

    BackupDescription: BackupDescriptionModel
