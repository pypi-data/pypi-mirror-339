from typing import Literal

from pydantic import BaseModel

from .point_in_time_recovery_description import (
    PointInTimeRecoveryDescription as PointInTimeRecoveryDescriptionModel,
)


class ContinuousBackupsDescription(BaseModel):
    """
    Represents the continuous backups and point in time recovery settings on the table.

    Attributes
    ----------
    ContinuousBackupsStatus : Literal["ENABLED", "DISABLED"]
        ContinuousBackupsStatus can be one of the following states: ENABLED, DISABLED.
    PointInTimeRecoveryDescription : Optional[PointInTimeRecoveryDescription]
        The description of the point in time recovery settings applied to the table.
    """

    ContinuousBackupsStatus: Literal["ENABLED", "DISABLED"]
    PointInTimeRecoveryDescription: PointInTimeRecoveryDescriptionModel | None = None
