# ruff: noqa: E501
from pydantic import BaseModel, constr


class DataSourceS3Configuration(BaseModel):
    """
    Configuration of an S3 location for a file which contains data to load.

    Attributes
    ----------
    BucketName : str
        The bucket name of the customer S3 bucket.
    ObjectKeyPrefix : str | None
        The prefix of the object key in the S3 bucket.
    """

    BucketName: constr(
        min_length=3, max_length=63, pattern=r"^[a-z0-9][\.\-a-z0-9]{1,61}[a-z0-9]$"
    )
    ObjectKeyPrefix: (
        constr(
            min_length=1,
            max_length=1024,
            pattern=r"^[a-zA-Z0-9|!\-_*'\(\)]([a-zA-Z0-9]|[!\-_*'\(\)\/.])+$",
        )
        | None
    ) = None
