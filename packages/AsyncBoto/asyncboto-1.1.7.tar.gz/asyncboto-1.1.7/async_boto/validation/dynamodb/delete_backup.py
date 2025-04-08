from pydantic import BaseModel, constr

from .data_types.backup_description import BackupDescription as BackupDescriptionModel


class DeleteBackupRequest(BaseModel):
    """
    Deletes an existing backup of a table.

    Attributes
    ----------
    BackupArn : str
        The ARN associated with the backup.
    """

    BackupArn: constr(min_length=37, max_length=1024)


class DeleteBackupResponse(BaseModel):
    """
    Response for the DeleteBackup operation.

    Attributes
    ----------
    BackupDescription : dict
        Contains the description of the backup created for the table.
    """

    BackupDescription: BackupDescriptionModel
