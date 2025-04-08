from pydantic import BaseModel


class LayerVersionContentInput(BaseModel):
    """
    A ZIP archive that contains the contents of an AWS Lambda layer.
    You can specify either an Amazon S3 location, or upload a layer archive directly.

    Parameters
    ----------
    S3Bucket : Optional[str]
        The Amazon S3 bucket of the layer archive.
    S3Key : Optional[str]
        The Amazon S3 key of the layer archive.
    S3ObjectVersion : Optional[str]
        For versioned objects, the version of the layer archive object to use.
    ZipFile : Optional[bytes]
        The base64-encoded contents of the layer archive. AWS SDK and AWS CLI clients
        handle the encoding for you.
    """

    S3Bucket: str | None = None
    S3Key: str | None = None
    S3ObjectVersion: str | None = None
    ZipFile: bytes | None = None
