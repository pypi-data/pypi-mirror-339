# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr

from .s3_bucket_source import S3BucketSource as S3BucketSourceModel


class ImportSummary(BaseModel):
    """
    Summary information about the source file for the import.

    Attributes
    ----------
    CloudWatchLogGroupArn : Optional[constr(min_length=1, max_length=1024)]
        The Amazon Resource Number (ARN) of the Cloudwatch Log Group associated with this import task.
    EndTime : Optional[datetime]
        The time at which this import task ended.
    ImportArn : Optional[constr(min_length=37, max_length=1024)]
        The Amazon Resource Number (ARN) corresponding to the import request.
    ImportStatus : Optional[Literal['IN_PROGRESS', 'COMPLETED', 'CANCELLING', 'CANCELLED', 'FAILED']]
        The status of the import operation.
    InputFormat : Optional[Literal['DYNAMODB_JSON', 'ION', 'CSV']]
        The format of the source data.
    S3BucketSource : Optional[S3BucketSource]
        The path and S3 bucket of the source file that is being imported.
    StartTime : Optional[datetime]
        The time at which this import task began.
    TableArn : Optional[constr(min_length=1, max_length=1024)]
        The Amazon Resource Number (ARN) of the table being imported into.
    """

    CloudWatchLogGroupArn: constr(min_length=1, max_length=1024) | None = None
    EndTime: datetime | None = None
    ImportArn: constr(min_length=37, max_length=1024) | None = None
    ImportStatus: (
        Literal["IN_PROGRESS", "COMPLETED", "CANCELLING", "CANCELLED", "FAILED"] | None
    ) = None
    InputFormat: Literal["DYNAMODB_JSON", "ION", "CSV"] | None = None
    S3BucketSource: S3BucketSourceModel | None = None
    StartTime: datetime | None = None
    TableArn: constr(min_length=1, max_length=1024) | None = None
