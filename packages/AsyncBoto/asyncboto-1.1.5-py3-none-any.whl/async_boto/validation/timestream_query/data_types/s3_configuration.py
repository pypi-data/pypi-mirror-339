# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, Field


class S3Configuration(BaseModel):
    """
    Details on S3 location for error reports that result from running a query.

    Parameters
    ----------
    BucketName : str
        Name of the S3 bucket under which error reports will be created.
    EncryptionOption : Optional[Literal['SSE_S3', 'SSE_KMS']], optional
        Encryption at rest options for the error reports. If no encryption option
        is specified, Timestream will choose SSE_S3 as default.
    ObjectKeyPrefix : Optional[str], optional
        Prefix for the error report key. Timestream by default adds the following
        prefix to the error report path.
    """

    BucketName: str = Field(
        min_length=3, max_length=63, pattern=r"[a-z0-9][\.\-a-z0-9]{1,61}[a-z0-9]"
    )
    EncryptionOption: Literal["SSE_S3", "SSE_KMS"] | None = None
    ObjectKeyPrefix: str | None = Field(
        None,
        min_length=1,
        max_length=896,
        pattern=r"[a-zA-Z0-9|!\-_*'\(\)]([a-zA-Z0-9]|[!\-_*'\(\)\/.])+",
    )
