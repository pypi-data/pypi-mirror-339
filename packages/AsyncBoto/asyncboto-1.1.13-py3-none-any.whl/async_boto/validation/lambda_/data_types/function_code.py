from typing import Annotated

from pydantic import BaseModel, Field


class FunctionCode(BaseModel):
    """
    The code for the Lambda function. Specifies deployment package details.

    Parameters
    ----------
    ImageUri : Optional[str], optional
        URI of a container image in the Amazon ECR registry.
    S3Bucket : Optional[str], optional
        An Amazon S3 bucket in the same AWS Region as the function.
    S3Key : Optional[str], optional
        The Amazon S3 key of the deployment package.
    S3ObjectVersion : Optional[str], optional
        For versioned objects, the version of the deployment package object to use.
    SourceKMSKeyArn : Optional[str], optional
        The ARN of the AWS KMS key used to encrypt the deployment package.
    ZipFile : Optional[bytes], optional
        The base64-encoded contents of the deployment package.
    """

    ImageUri: str | None = None
    S3Bucket: Annotated[
        str | None,
        Field(min_length=3, max_length=63),
    ] = None
    S3Key: Annotated[str | None, Field(min_length=1, max_length=1024)] = None
    S3ObjectVersion: Annotated[str | None, Field(min_length=1, max_length=1024)] = None
    SourceKMSKeyArn: str | None = None
    ZipFile: bytes | None = None
