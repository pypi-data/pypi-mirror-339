# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr


class S3Configuration(BaseModel):
    """
    The configuration that specifies an S3 location.

    Attributes
    ----------
    BucketName : str | None
        The bucket name of the customer S3 bucket.
    EncryptionOption : str | None
        The encryption option for the customer S3 location.
    KmsKeyId : str | None
        The AWS KMS key ID for the customer S3 location when encrypting with an AWS managed key.
    ObjectKeyPrefix : str | None
        The object key preview for the customer S3 location.
    """

    BucketName: (
        constr(
            min_length=3, max_length=63, pattern=r"[a-z0-9][\.\-a-z0-9]{1,61}[a-z0-9]"
        )
        | None
    ) = None
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
