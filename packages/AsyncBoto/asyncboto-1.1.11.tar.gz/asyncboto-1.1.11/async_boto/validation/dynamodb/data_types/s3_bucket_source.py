from pydantic import BaseModel, constr


class S3BucketSource(BaseModel):
    """
    The S3 bucket that is being imported from.

    Attributes
    ----------
    S3Bucket : str
        The S3 bucket that is being imported from.
    S3BucketOwner : Optional[str]
        The account number of the S3 bucket that is being imported from.
    S3KeyPrefix : Optional[str]
        The key prefix shared by all S3 Objects that are being imported.
    """

    S3Bucket: constr(max_length=255, pattern=r"^[a-z0-9A-Z]+[\.\-\w]*[a-z0-9A-Z]+$")
    S3BucketOwner: constr(pattern=r"^[0-9]{12}$") | None = None
    S3KeyPrefix: constr(max_length=1024) | None = None
