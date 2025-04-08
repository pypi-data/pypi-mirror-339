from pydantic import BaseModel


class Layer(BaseModel):
    """
    An AWS Lambda layer.

    Parameters
    ----------
    Arn : Optional[str]
        The Amazon Resource Name (ARN) of the function layer.
    CodeSize : Optional[int]
        The size of the layer archive in bytes.
    SigningJobArn : Optional[str]
        The Amazon Resource Name (ARN) of a signing job.
    SigningProfileVersionArn : Optional[str]
        The Amazon Resource Name (ARN) for a signing profile version.
    """

    Arn: str | None = None
    CodeSize: int | None = None
    SigningJobArn: str | None = None
    SigningProfileVersionArn: str | None = None
