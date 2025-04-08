# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, conint, constr

from .incremental_export_specification import (
    IncrementalExportSpecification as IncrementalExportSpecificationModel,
)


class ExportDescription(BaseModel):
    r"""
    Represents the properties of the exported table.

    Attributes
    ----------
    BilledSizeBytes : Optional[conint(ge=0)]
        The billable size of the table export.
    ClientToken : Optional[constr(pattern=r'^[^\$]+$')]
        The client token that was provided for the export task.
    EndTime : Optional[datetime]
        The time at which the export task completed.
    ExportArn : Optional[constr(min_length=37, max_length=1024)]
        The Amazon Resource Name (ARN) of the table export.
    ExportFormat : Optional[Literal["DYNAMODB_JSON", "ION"]]
        The format of the exported data.
    ExportManifest : Optional[str]
        The name of the manifest file for the export task.
    ExportStatus : Optional[Literal["IN_PROGRESS", "COMPLETED", "FAILED"]]
        Export can be in one of the following states: IN_PROGRESS, COMPLETED, or FAILED.
    ExportTime : Optional[datetime]
        Point in time from which table data was exported.
    ExportType : Optional[Literal["FULL_EXPORT", "INCREMENTAL_EXPORT"]]
        The type of export that was performed.
    FailureCode : Optional[str]
        Status code for the result of the failed export.
    FailureMessage : Optional[str]
        Export failure reason description.
    IncrementalExportSpecification : Optional[IncrementalExportSpecificationModel]
        Optional object containing the parameters specific to an incremental export.
    ItemCount : Optional[conint(ge=0)]
        The number of items exported.
    S3Bucket : Optional[constr(max_length=255, pattern=r'^[a-z0-9A-Z]+[\.\-\w]*[a-z0-9A-Z]+$')]
        The name of the Amazon S3 bucket containing the export.
    S3BucketOwner : Optional[constr(pattern=r'[0-9]{12}')]
        The ID of the AWS account that owns the bucket containing the export.
    S3Prefix : Optional[constr(max_length=1024)]
        The Amazon S3 bucket prefix used as the file name and path of the exported snapshot.
    S3SseAlgorithm : Optional[Literal["AES256", "KMS"]]
        Type of encryption used on the bucket where export data is stored.
    S3SseKmsKeyId : Optional[constr(min_length=1, max_length=2048)]
        The ID of the AWS KMS managed key used to encrypt the S3 bucket where export data is stored (if applicable).
    StartTime : Optional[datetime]
        The time at which the export task began.
    TableArn : Optional[constr(min_length=1, max_length=1024)]
        The Amazon Resource Name (ARN) of the table that was exported.
    TableId : Optional[constr(pattern=r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')]
        Unique ID of the table that was exported.
    """

    BilledSizeBytes: conint(ge=0) | None = None
    ClientToken: constr(pattern=r"^[^\$]+$") | None = None
    EndTime: datetime | None = None
    ExportArn: constr(min_length=37, max_length=1024) | None = None
    ExportFormat: Literal["DYNAMODB_JSON", "ION"] | None = None
    ExportManifest: str | None = None
    ExportStatus: Literal["IN_PROGRESS", "COMPLETED", "FAILED"] | None = None
    ExportTime: datetime | None = None
    ExportType: Literal["FULL_EXPORT", "INCREMENTAL_EXPORT"] | None = None
    FailureCode: str | None = None
    FailureMessage: str | None = None
    IncrementalExportSpecification: IncrementalExportSpecificationModel | None = None
    ItemCount: conint(ge=0) | None = None
    S3Bucket: (
        constr(max_length=255, pattern=r"^[a-z0-9A-Z]+[\.\-\w]*[a-z0-9A-Z]+$") | None
    ) = None
    S3BucketOwner: constr(pattern=r"[0-9]{12}") | None = None
    S3Prefix: constr(max_length=1024) | None = None
    S3SseAlgorithm: Literal["AES256", "KMS"] | None = None
    S3SseKmsKeyId: constr(min_length=1, max_length=2048) | None = None
    StartTime: datetime | None = None
    TableArn: constr(min_length=1, max_length=1024) | None = None
    TableId: (
        constr(pattern=r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
        | None
    ) = None
