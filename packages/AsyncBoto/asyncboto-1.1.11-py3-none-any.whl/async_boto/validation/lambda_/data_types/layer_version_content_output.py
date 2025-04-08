from pydantic import BaseModel


class LayerVersionContentOutput(BaseModel):
    """
    Details about a version of an AWS Lambda layer.

    Attributes
    ----------
    CodeSha256 : Optional[str]
        The SHA-256 hash of the layer archive.
    CodeSize : Optional[int]
        The size of the layer archive in bytes.
    Location : Optional[str]
        A link to the layer archive in Amazon S3 that is valid for 10 minutes.
    SigningJobArn : Optional[str]
        The Amazon Resource Name (ARN) of a signing job.
    SigningProfileVersionArn : Optional[str]
        The Amazon Resource Name (ARN) for a signing profile version.
    """

    CodeSha256: str | None = None
    CodeSize: int | None = None
    Location: str | None = None
    SigningJobArn: str | None = None
    SigningProfileVersionArn: str | None = None
