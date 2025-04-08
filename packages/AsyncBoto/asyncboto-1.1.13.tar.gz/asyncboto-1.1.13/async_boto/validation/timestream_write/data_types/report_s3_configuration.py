# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr


class ReportS3Configuration(BaseModel):
    """
    Configuration of an S3 location to write error reports and events for a batch load.

    Attributes
    ----------
    BucketName : str
        The name of the S3 bucket.
    EncryptionOption : str | None
        The encryption option for the S3 bucket.
    KmsKeyId : str | None
        The KMS key ID for the S3 bucket.
    ObjectKeyPrefix : str | None
        The object key prefix for the S3 bucket.
    """

    BucketName: constr(
        min_length=3, max_length=63, pattern=r"[a-z0-9][\.\-a-z0-9]{1,61}[a-z0-9]"
    )
    EncryptionOption: Literal["SSE_S3", "SSE_KMS"] | None = None
    KmsKeyId: constr(min_length=1, max_length=2048) | None = None
    ObjectKeyPrefix: (
        constr(
            min_length=1,
            max_length=928,
            pattern=r"[a-zA-Z0-9|!\-_*'\(\)]([a-zA-Z0-9]|[!\-_*'\(\)\/.])+",
        )
        | None
    ) = None
