# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr


class BatchLoadTask(BaseModel):
    """
    Details about a batch load task.

    Attributes
    ----------
    CreationTime : datetime | None
        The time when the Timestream batch load task was created.
    DatabaseName : str | None
        Database name for the database into which a batch load task loads data.
    LastUpdatedTime : datetime | None
        The time when the Timestream batch load task was last updated.
    ResumableUntil : datetime | None
        The time until the batch load task is resumable.
    TableName : str | None
        Table name for the table into which a batch load task loads data.
    TaskId : str | None
        The ID of the batch load task.
    TaskStatus : Literal["CREATED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "PROGRESS_STOPPED", "PENDING_RESUME"] | None
        Status of the batch load task.
    """

    CreationTime: datetime | None = None
    DatabaseName: str | None = None
    LastUpdatedTime: datetime | None = None
    ResumableUntil: datetime | None = None
    TableName: str | None = None
    TaskId: constr(min_length=3, max_length=32, pattern=r"^[A-Z0-9]+$") | None = None
    TaskStatus: (
        Literal[
            "CREATED",
            "IN_PROGRESS",
            "FAILED",
            "SUCCEEDED",
            "PROGRESS_STOPPED",
            "PENDING_RESUME",
        ]
        | None
    ) = None
