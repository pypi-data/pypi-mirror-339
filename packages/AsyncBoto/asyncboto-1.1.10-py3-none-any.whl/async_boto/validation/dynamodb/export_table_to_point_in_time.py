from typing import Literal

from pydantic import BaseModel, conint, constr

from .data_types.export_description import ExportDescription as ExportDescriptionModel
from .data_types.incremental_export_specification import (
    IncrementalExportSpecification as IncrementalExportSpecificationModel,
)


class ExportTableToPointInTimeRequest(BaseModel):
    """
    Exports table data to an S3 bucket.

    Attributes
    ----------
    S3Bucket : str
        The name of the Amazon S3 bucket to export the snapshot to.
    TableArn : str
        The Amazon Resource Name (ARN) associated with the table to export.
    ClientToken : Optional[str]
        Providing a ClientToken makes the call idempotent.
    ExportFormat : Optional[Literal['DYNAMODB_JSON', 'ION']]
        The format for the exported data.
    ExportTime : Optional[int]
        Time in the past from which to export table data, counted in seconds from the
        start of the Unix epoch.
    ExportType : Optional[Literal['FULL_EXPORT', 'INCREMENTAL_EXPORT']]
        Choice of whether to execute as a full export or incremental export.
    IncrementalExportSpecification : Optional[IncrementalExportSpecification]
        Optional object containing the parameters specific to an incremental export.
    S3BucketOwner : Optional[constr(regex=r'^[0-9]{12}$')]
        The ID of the AWS account that owns the bucket the export will be stored in.
    S3Prefix : Optional[constr(max_length=1024)]
        The Amazon S3 bucket prefix to use as the file name and path of the exported
        snapshot.
    S3SseAlgorithm : Optional[Literal['AES256', 'KMS']]
        Type of encryption used on the bucket where export data will be stored.
    S3SseKmsKeyId : Optional[constr(min_length=1, max_length=2048)]
        The ID of the AWS KMS managed key used to encrypt the S3 bucket where export
        data will be stored (if applicable).
    """

    S3Bucket: constr(max_length=255, pattern=r"^[a-z0-9A-Z]+[\.\-\w]*[a-z0-9A-Z]+$")
    TableArn: constr(min_length=1, max_length=1024)
    ClientToken: constr(pattern=r"^[^\$]+$") | None = None
    ExportFormat: Literal["DYNAMODB_JSON", "ION"] | None = None
    ExportTime: conint(ge=0) | None = None
    ExportType: Literal["FULL_EXPORT", "INCREMENTAL_EXPORT"] | None = None
    IncrementalExportSpecification: IncrementalExportSpecificationModel | None = None
    S3BucketOwner: constr(pattern=r"^[0-9]{12}$") | None = None
    S3Prefix: constr(max_length=1024) | None = None
    S3SseAlgorithm: Literal["AES256", "KMS"] | None = None
    S3SseKmsKeyId: constr(min_length=1, max_length=2048) | None = None


class ExportTableToPointInTimeResponse(BaseModel):
    """
    Response for the ExportTableToPointInTime operation.

    Attributes
    ----------
    ExportDescription : Optional[ExportDescription]
        Contains a description of the table export.
    """

    ExportDescription: ExportDescriptionModel | None = None
