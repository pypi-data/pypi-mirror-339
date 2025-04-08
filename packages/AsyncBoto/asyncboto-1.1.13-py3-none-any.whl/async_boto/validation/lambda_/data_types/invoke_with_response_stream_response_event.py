from invoke_response_stream_update import InvokeResponseStreamUpdate
from invoke_with_response_stream_complete_event import (
    InvokeWithResponseStreamCompleteEvent,
)
from pydantic import BaseModel


class InvokeWithResponseStreamResponseEvent(BaseModel):
    """
    An object that includes a chunk of the response payload. When the stream has ended,
    Lambda includes a InvokeComplete object.

    Parameters
    ----------
    InvokeComplete : Optional[InvokeWithResponseStreamCompleteEvent]
        An object that's returned when the stream has ended and all the payload chunks
        have been returned.
    PayloadChunk : Optional[InvokeResponseStreamUpdate]
        A chunk of the streamed response payload.
    """

    InvokeComplete: InvokeWithResponseStreamCompleteEvent | None = None
    PayloadChunk: InvokeResponseStreamUpdate | None = None
