from pydantic import BaseModel, constr

from .data_types.continuous_backups_description import (
    ContinuousBackupsDescription as ContinuousBackupsDescriptionModel,
)


class DescribeContinuousBackupsRequest(BaseModel):
    """
    Checks the status of continuous backups and point in time recovery on the
    specified table.

    Attributes
    ----------
    TableName : str
        Name of the table for which the customer wants to check the continuous backups
        and point in time recovery settings.
    """

    TableName: constr(min_length=1, max_length=1024)


class DescribeContinuousBackupsResponse(BaseModel):
    """
    Response for the DescribeContinuousBackups operation.

    Attributes
    ----------
    ContinuousBackupsDescription : ContinuousBackupsDescription
        Represents the continuous backups and point in time recovery settings on the
        specified table.
    """

    ContinuousBackupsDescription: ContinuousBackupsDescriptionModel
