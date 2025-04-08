from pydantic import BaseModel


class ImageConfigError(BaseModel):
    """
    Error response for image configuration in a Lambda function.

    Parameters
    ----------
    ErrorCode : Optional[str], optional
        The error code for the configuration error.
    Message : Optional[str], optional
        The detailed error message.
    """

    ErrorCode: str | None = None
    Message: str | None = None
