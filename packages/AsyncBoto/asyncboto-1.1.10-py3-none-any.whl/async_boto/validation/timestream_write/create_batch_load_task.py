from pydantic import BaseModel, conint, constr

from .data_types.data_model_configuration import DataModelConfiguration
from .data_types.data_source_configuration import DataSourceConfiguration
from .data_types.report_configuration import ReportConfiguration


class CreateBatchLoadTaskRequest(BaseModel):
    """
    Creates a new Timestream batch load task. A batch load task processes data from a
    CSV source in an S3 location and writes to a Timestream table.
    A mapping from source to target is defined in a batch load task.
    Errors and events are written to a report at an S3 location.

    Attributes
    ----------
    ClientToken : str | None
        A unique token to ensure idempotency.
    DataModelConfiguration : DataModelConfiguration | None
        Configuration for the data model.
    DataSourceConfiguration : DataSourceConfiguration
        Configuration details about the data source for a batch load task.
    RecordVersion : int | None
        The version of the record.
    ReportConfiguration : ReportConfiguration
        Report configuration for a batch load task.
    TargetDatabaseName : str
        Target Timestream database for a batch load task.
    TargetTableName : str
        Target Timestream table for a batch load task.
    """

    ClientToken: constr(min_length=1, max_length=64) | None = None
    DataModelConfiguration: DataModelConfiguration | None = None
    DataSourceConfiguration: DataSourceConfiguration
    RecordVersion: conint(ge=1) | None = None
    ReportConfiguration: ReportConfiguration
    TargetDatabaseName: constr(pattern=r"[a-zA-Z0-9_.-]+")
    TargetTableName: constr(pattern=r"[a-zA-Z0-9_.-]+")


class CreateBatchLoadTaskResponse(BaseModel):
    """
    The response returned by the service when a CreateBatchLoadTask action is
    successful.

    Attributes
    ----------
    TaskId : str
        The ID of the batch load task.
    """

    TaskId: constr(min_length=3, max_length=32, pattern=r"[A-Z0-9]+")
