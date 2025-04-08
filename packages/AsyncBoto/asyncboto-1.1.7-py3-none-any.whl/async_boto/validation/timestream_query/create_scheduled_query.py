# ruff: noqa: E501
from pydantic import BaseModel, Field, constr

from .data_types.error_report_configuration import ErrorReportConfiguration
from .data_types.notification_configuration import NotificationConfiguration
from .data_types.schedule_configuration import ScheduleConfiguration
from .data_types.tag import Tag
from .data_types.target_configuration import TargetConfiguration


class CreateScheduledQueryRequest(BaseModel):
    """
    Creates a scheduled query that will be run on your behalf at the configured schedule.

    Attributes
    ----------
    ClientToken : str | None
        Using a ClientToken makes the call to CreateScheduledQuery idempotent.
    ErrorReportConfiguration : ErrorReportConfiguration
        Configuration for error reporting.
    KmsKeyId : str | None
        The Amazon KMS key used to encrypt the scheduled query resource, at-rest.
    Name : str
        Name of the scheduled query.
    NotificationConfiguration : NotificationConfiguration
        Notification configuration for the scheduled query.
    QueryString : str
        The query string to run.
    ScheduleConfiguration : ScheduleConfiguration
        The schedule configuration for the query.
    ScheduledQueryExecutionRoleArn : str
        The ARN for the IAM role that Timestream will assume when running the scheduled query.
    Tags : List[Tag] | None
        A list of key-value pairs to label the scheduled query.
    TargetConfiguration : TargetConfiguration | None
        Configuration used for writing the result of a query.
    """

    ClientToken: constr(min_length=32, max_length=128) | None = None
    ErrorReportConfiguration: ErrorReportConfiguration
    KmsKeyId: constr(min_length=1, max_length=2048) | None = None
    Name: constr(
        min_length=1,
        max_length=64,
        pattern=r"[a-zA-Z0-9|!\-_*'\(\)]([a-zA-Z0-9]|[!\-_*'\(\)\/.])+",
    )
    NotificationConfiguration: NotificationConfiguration
    QueryString: constr(min_length=1, max_length=262144)
    ScheduleConfiguration: ScheduleConfiguration
    ScheduledQueryExecutionRoleArn: constr(min_length=1, max_length=2048)
    Tags: list[Tag] | None = Field(None, max_length=200)
    TargetConfiguration: TargetConfiguration | None = None


class CreateScheduledQueryResponse(BaseModel):
    """
    The response returned by the service when a CreateScheduledQuery action is
    successful.

    Attributes
    ----------
    Arn : str
        ARN for the created scheduled query.
    """

    Arn: constr(min_length=1, max_length=2048)
