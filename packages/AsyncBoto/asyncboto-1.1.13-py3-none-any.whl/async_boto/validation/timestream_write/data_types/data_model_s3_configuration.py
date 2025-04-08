# ruff: noqa: E501
from pydantic import BaseModel, constr


class DataModelS3Configuration(BaseModel):
    """
    S3 configuration for the data model.

    Attributes
    ----------
    BucketName : str | None
        The name of the S3 bucket.
    ObjectKey : str | None
        The key of the object in the S3 bucket.
    """

    BucketName: (
        constr(
            min_length=3, max_length=63, pattern=r"^[a-z0-9][\.\-a-z0-9]{1,61}[a-z0-9]$"
        )
        | None
    ) = None
    ObjectKey: (
        constr(
            min_length=1,
            max_length=1024,
            pattern=r"^[a-zA-Z0-9|!\-_*'\(\)]([a-zA-Z0-9]|[!\-_*'\(\)\/.])+$",
        )
        | None
    ) = None
