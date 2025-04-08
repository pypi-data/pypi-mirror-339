# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from .error_report_configuration import ErrorReportConfiguration
from .notification_configuration import NotificationConfiguration
from .schedule_configuration import ScheduleConfiguration
from .scheduled_query_run_summary import ScheduledQueryRunSummary
from .target_configuration import TargetConfiguration


class ScheduledQueryDescription(BaseModel):
    """
    Structure that describes scheduled query.

    Parameters
    ----------
    Arn : str
        Scheduled query ARN.
    Name : str
        Name of the scheduled query.
    NotificationConfiguration : NotificationConfiguration
        Notification configuration.
    QueryString : str
        The query to be run.
    ScheduleConfiguration : ScheduleConfiguration
        Schedule configuration.
    State : Literal['ENABLED', 'DISABLED']
        State of the scheduled query.
    CreationTime : Optional[datetime], optional
        Creation time of the scheduled query.
    ErrorReportConfiguration : Optional[ErrorReportConfiguration], optional
        Error-reporting configuration for the scheduled query.
    KmsKeyId : Optional[str], optional
        A customer provided KMS key used to encrypt the scheduled query resource.
    LastRunSummary : Optional[ScheduledQueryRunSummary], optional
        Runtime summary for the last scheduled query run.
    NextInvocationTime : Optional[datetime], optional
        The next time the scheduled query is scheduled to run.
    PreviousInvocationTime : Optional[datetime], optional
        Last time the query was run.
    RecentlyFailedRuns : Optional[List[ScheduledQueryRunSummary]], optional
        Runtime summary for the last five failed scheduled query runs.
    ScheduledQueryExecutionRoleArn : Optional[str], optional
        IAM role that Timestream uses to run the schedule query.
    TargetConfiguration : Optional[TargetConfiguration], optional
        Scheduled query target store configuration.
    """

    Arn: str = Field(min_length=1, max_length=2048)
    Name: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"[a-zA-Z0-9|!\-_*'\(\)]([a-zA-Z0-9]|[!\-_*'\(\)\/.])+",
    )
    NotificationConfiguration: NotificationConfiguration
    QueryString: str = Field(min_length=1, max_length=262144)
    ScheduleConfiguration: ScheduleConfiguration
    State: Literal["ENABLED", "DISABLED"]
    CreationTime: datetime | None = None
    ErrorReportConfiguration: ErrorReportConfiguration | None = None
    KmsKeyId: str | None = Field(None, min_length=1, max_length=2048)
    LastRunSummary: ScheduledQueryRunSummary | None = None
    NextInvocationTime: datetime | None = None
    PreviousInvocationTime: datetime | None = None
    RecentlyFailedRuns: list[ScheduledQueryRunSummary] | None = None
    ScheduledQueryExecutionRoleArn: str | None = Field(
        None, min_length=1, max_length=2048
    )
    TargetConfiguration: TargetConfiguration | None = None
