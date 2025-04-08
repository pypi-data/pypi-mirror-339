# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr

from .batch_load_progress_report import BatchLoadProgressReport
from .data_model_configuration import DataModelConfiguration
from .data_source_configuration import DataSourceConfiguration
from .report_configuration import ReportConfiguration


class BatchLoadTaskDescription(BaseModel):
    """
    Details about a batch load task.

    Attributes
    ----------
    CreationTime : datetime | None
        The time when the Timestream batch load task was created.
    DataModelConfiguration : DataModelConfiguration | None
        Data model configuration for a batch load task.
    DataSourceConfiguration : DataSourceConfiguration | None
        Configuration details about the data source for a batch load task.
    ErrorMessage : str | None
        Error message for the batch load task.
    LastUpdatedTime : datetime | None
        The time when the Timestream batch load task was last updated.
    ProgressReport : BatchLoadProgressReport | None
        Progress report for the batch load task.
    RecordVersion : int | None
        Record version for the batch load task.
    ReportConfiguration : ReportConfiguration | None
        Report configuration for the batch load task.
    ResumableUntil : datetime | None
        The time until the batch load task is resumable.
    TargetDatabaseName : str | None
        Target database name for the batch load task.
    TargetTableName : str | None
        Target table name for the batch load task.
    TaskId : str | None
        The ID of the batch load task.
    TaskStatus : Literal["CREATED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "PROGRESS_STOPPED", "PENDING_RESUME"] | None
        Status of the batch load task.
    """

    CreationTime: datetime | None = None
    DataModelConfiguration: DataModelConfiguration | None = None
    DataSourceConfiguration: DataSourceConfiguration | None = None
    ErrorMessage: constr(min_length=1, max_length=2048) | None = None
    LastUpdatedTime: datetime | None = None
    ProgressReport: BatchLoadProgressReport | None = None
    RecordVersion: int | None = None
    ReportConfiguration: ReportConfiguration | None = None
    ResumableUntil: datetime | None = None
    TargetDatabaseName: str | None = None
    TargetTableName: str | None = None
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
