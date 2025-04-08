from pydantic import BaseModel, constr

from .data_types.backup_details import BackupDetails as BackupDetailsModel


class CreateBackupRequest(BaseModel):
    """
    Creates a backup for an existing table.

    Attributes
    ----------
    BackupName : str
        Specified name for the backup.
    TableName : str
        The name of the table. You can also provide the Amazon Resource Name
        (ARN) of the table in this parameter.
    """

    BackupName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    TableName: constr(min_length=1, max_length=1024)


class CreateBackupResponse(BaseModel):
    """
    Response for the CreateBackup operation.

    Attributes
    ----------
    BackupDetails : BackupDetails
        Contains the details of the backup created for the table.
    """

    BackupDetails: BackupDetailsModel
