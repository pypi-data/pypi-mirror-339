from pydantic import BaseModel


class FunctionCodeLocation(BaseModel):
    """
    Details about a function's deployment package location.

    Parameters
    ----------
    ImageUri : Optional[str], optional
        URI of a container image in the Amazon ECR registry.
    Location : Optional[str], optional
        A presigned URL to download the deployment package.
    RepositoryType : Optional[str], optional
        The service hosting the file.
    ResolvedImageUri : Optional[str], optional
        The resolved URI for the image.
    SourceKMSKeyArn : Optional[str], optional
        The ARN of the AWS KMS key used to encrypt the deployment package.
    """

    ImageUri: str | None = None
    Location: str | None = None
    RepositoryType: str | None = None
    ResolvedImageUri: str | None = None
    SourceKMSKeyArn: str | None = None
