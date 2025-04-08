from pydantic import BaseModel, constr

from .data_types.continuous_backups_description import (
    ContinuousBackupsDescription as ContinuousBackupsDescriptionModel,
)
from .data_types.point_in_time_recovery_specification import (
    PointInTimeRecoverySpecification as PointInTimeRecoverySpecificationModel,
)


class UpdateContinuousBackupsRequest(BaseModel):
    """
    Request model for the UpdateContinuousBackups operation.

    Attributes
    ----------
    PointInTimeRecoverySpecification : PointInTimeRecoverySpecification
        Represents the settings used to enable point in time recovery.
    TableName : str
        The name of the table or its ARN.
    """

    PointInTimeRecoverySpecification: PointInTimeRecoverySpecificationModel
    TableName: constr(min_length=1, max_length=1024)


class UpdateContinuousBackupsResponse(BaseModel):
    """
    Response model for the UpdateContinuousBackups operation.

    Attributes
    ----------
    ContinuousBackupsDescription : ContinuousBackupsDescription
        Represents the continuous backups and point in time recovery settings on
        the table.
    """

    ContinuousBackupsDescription: ContinuousBackupsDescriptionModel | None = None
