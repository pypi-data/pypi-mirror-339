from datetime import datetime
from typing import Literal

from pydantic import BaseModel, conint


class PointInTimeRecoveryDescription(BaseModel):
    """
    The description of the point in time settings applied to the table.

    Attributes
    ----------
    EarliestRestorableDateTime : Optional[datetime]
        Specifies the earliest point in time you can restore your table to.
    LatestRestorableDateTime : Optional[datetime]
        LatestRestorableDateTime is typically 5 minutes before the current time.
    PointInTimeRecoveryStatus : Optional[str]
        The current state of point in time recovery.
    RecoveryPeriodInDays : Optional[int]
        The number of preceding days for which continuous backups are taken and
        maintained.
    """

    EarliestRestorableDateTime: datetime | None = None
    LatestRestorableDateTime: datetime | None = None
    PointInTimeRecoveryStatus: Literal["ENABLED", "DISABLED"] | None = None
    RecoveryPeriodInDays: conint(ge=1, le=35) | None = None
