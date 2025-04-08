# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, conint, constr

from .input_format_options import InputFormatOptions as InputFormatOptionsModel
from .s3_bucket_source import S3BucketSource as S3BucketSourceModel
from .table_creation_parameters import (
    TableCreationParameters as TableCreationParametersModel,
)


class ImportTableDescription(BaseModel):
    r"""
    Represents the properties of the table being imported into.

    Attributes
    ----------
    ClientToken : Optional[constr(regex=r'^[^\$]+$')]
        The client token that was provided for the import task.
    CloudWatchLogGroupArn : Optional[constr(min_length=1, max_length=1024)]
        The Amazon Resource Number (ARN) of the Cloudwatch Log Group associated with the target table.
    EndTime : Optional[datetime]
        The time at which the creation of the table associated with this import task completed.
    ErrorCount : Optional[conint(ge=0)]
        The number of errors occurred on importing the source file into the target table.
    FailureCode : Optional[str]
        The error code corresponding to the failure that the import job ran into during execution.
    FailureMessage : Optional[str]
        The error message corresponding to the failure that the import job ran into during execution.
    ImportArn : Optional[constr(min_length=37, max_length=1024)]
        The Amazon Resource Number (ARN) corresponding to the import request.
    ImportedItemCount : Optional[conint(ge=0)]
        The number of items successfully imported into the new table.
    ImportStatus : Optional[Literal['IN_PROGRESS', 'COMPLETED', 'CANCELLING', 'CANCELLED', 'FAILED']]
        The status of the import.
    InputCompressionType : Optional[Literal['GZIP', 'ZSTD', 'NONE']]
        The compression options for the data that has been imported into the target table.
    InputFormat : Optional[Literal['DYNAMODB_JSON', 'ION', 'CSV']]
        The format of the source data going into the target table.
    InputFormatOptions : Optional[InputFormatOptions]
        The format options for the data that was imported into the target table.
    ProcessedItemCount : Optional[conint(ge=0)]
        The total number of items processed from the source file.
    ProcessedSizeBytes : Optional[conint(ge=0)]
        The total size of data processed from the source file, in Bytes.
    S3BucketSource : Optional[S3BucketSource]
        Values for the S3 bucket the source file is imported from.
    StartTime : Optional[datetime]
        The time when this import task started.
    TableArn : Optional[constr(min_length=1, max_length=1024)]
        The Amazon Resource Number (ARN) of the table being imported into.
    TableCreationParameters : Optional[TableCreationParameters]
        The parameters for the new table that is being imported into.
    TableId : Optional[constr(regex=r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')]
        The table id corresponding to the table created by import table process.
    """

    ClientToken: constr(pattern=r"^[^\$]+$") | None = None
    CloudWatchLogGroupArn: constr(min_length=1, max_length=1024) | None = None
    EndTime: datetime | None = None
    ErrorCount: conint(ge=0) | None = None
    FailureCode: str | None = None
    FailureMessage: str | None = None
    ImportArn: constr(min_length=37, max_length=1024) | None = None
    ImportedItemCount: conint(ge=0) | None = None
    ImportStatus: (
        Literal["IN_PROGRESS", "COMPLETED", "CANCELLING", "CANCELLED", "FAILED"] | None
    ) = None
    InputCompressionType: Literal["GZIP", "ZSTD", "NONE"] | None = None
    InputFormat: Literal["DYNAMODB_JSON", "ION", "CSV"] | None = None
    InputFormatOptions: InputFormatOptionsModel | None = None
    ProcessedItemCount: conint(ge=0) | None = None
    ProcessedSizeBytes: conint(ge=0) | None = None
    S3BucketSource: S3BucketSourceModel | None = None
    StartTime: datetime | None = None
    TableArn: constr(min_length=1, max_length=1024) | None = None
    TableCreationParameters: TableCreationParametersModel | None = None
    TableId: (
        constr(pattern=r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
        | None
    ) = None
