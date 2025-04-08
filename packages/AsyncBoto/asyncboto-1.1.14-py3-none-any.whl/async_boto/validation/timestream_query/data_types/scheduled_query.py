# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from .error_report_configuration import ErrorReportConfiguration
from .target_destination import TargetDestination


class ScheduledQuery(BaseModel):
    """
    Scheduled Query

    Parameters
    ----------
    Arn : str
        The Amazon Resource Name.
    Name : str
        The name of the scheduled query.
    State : Literal['ENABLED', 'DISABLED']
        State of scheduled query.
    CreationTime : Optional[datetime], optional
        The creation time of the scheduled query.
    ErrorReportConfiguration : Optional[ErrorReportConfiguration], optional
        Configuration for scheduled query error reporting.
    LastRunStatus : Optional[Literal['AUTO_TRIGGER_SUCCESS', 'AUTO_TRIGGER_FAILURE', 'MANUAL_TRIGGER_SUCCESS', 'MANUAL_TRIGGER_FAILURE']], optional
        Status of the last scheduled query run.
    NextInvocationTime : Optional[datetime], optional
        The next time the scheduled query is to be run.
    PreviousInvocationTime : Optional[datetime], optional
        The last time the scheduled query was run.
    TargetDestination : Optional[TargetDestination], optional
        Target data source where final scheduled query result will be written.
    """

    Arn: str = Field(min_length=1, max_length=2048)
    Name: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"[a-zA-Z0-9|!\-_*'\(\)]([a-zA-Z0-9]|[!\-_*'\(\)\/.])+",
    )
    State: Literal["ENABLED", "DISABLED"]
    CreationTime: datetime | None = None
    ErrorReportConfiguration: ErrorReportConfiguration | None = None
    LastRunStatus: (
        Literal[
            "AUTO_TRIGGER_SUCCESS",
            "AUTO_TRIGGER_FAILURE",
            "MANUAL_TRIGGER_SUCCESS",
            "MANUAL_TRIGGER_FAILURE",
        ]
        | None
    ) = None
    NextInvocationTime: datetime | None = None
    PreviousInvocationTime: datetime | None = None
    TargetDestination: TargetDestination | None = None
