from pydantic import BaseModel


class RuntimeVersionError(BaseModel):
    """
    Error response when Lambda is unable to retrieve the runtime version for a function.

    Attributes
    ----------
    ErrorCode : Optional[str]
        The error code.
    Message : Optional[str]
        The error message.
    """

    ErrorCode: str | None = None
    Message: str | None = None
