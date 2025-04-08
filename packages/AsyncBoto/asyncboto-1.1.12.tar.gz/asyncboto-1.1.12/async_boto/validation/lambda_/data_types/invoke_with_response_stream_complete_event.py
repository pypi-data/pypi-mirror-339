from pydantic import BaseModel


class InvokeWithResponseStreamCompleteEvent(BaseModel):
    """
    A response confirming that the event stream is complete.

    Parameters
    ----------
    ErrorCode : Optional[str]
        An error code.
    ErrorDetails : Optional[str]
        The details of any returned error.
    LogResult : Optional[str]
        The last 4 KB of the execution log, which is base64-encoded.
    """

    ErrorCode: str | None = None
    ErrorDetails: str | None = None
    LogResult: str | None = None
