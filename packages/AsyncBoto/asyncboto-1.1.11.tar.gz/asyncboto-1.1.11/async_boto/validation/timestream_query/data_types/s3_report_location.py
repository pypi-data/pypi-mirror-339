from pydantic import BaseModel, Field


class S3ReportLocation(BaseModel):
    """
    S3 report location for the scheduled query run.

    Parameters
    ----------
    BucketName : Optional[str], optional
        S3 bucket name.
    ObjectKey : Optional[str], optional
        S3 key.
    """

    BucketName: str | None = Field(
        None, min_length=3, max_length=63, pattern=r"[a-z0-9][\.\-a-z0-9]{1,61}[a-z0-9]"
    )
    ObjectKey: str | None = None
