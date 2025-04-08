from pydantic import BaseModel


class InvokeResponseStreamUpdate(BaseModel):
    """
    A chunk of the streamed response payload.

    Parameters
    ----------
    Payload : Optional[bytes]
        Data returned by your Lambda function.
    """

    Payload: bytes | None = None
