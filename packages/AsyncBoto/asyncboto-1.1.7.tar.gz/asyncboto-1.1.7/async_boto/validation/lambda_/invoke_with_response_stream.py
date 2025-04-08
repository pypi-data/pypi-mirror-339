from typing import Literal

from pydantic import BaseModel, constr

from .data_types.invoke_response_stream_update import InvokeResponseStreamUpdate
from .data_types.invoke_with_response_stream_complete_event import (
    InvokeWithResponseStreamCompleteEvent,
)


class InvokeWithResponseStreamRequest(BaseModel):
    """
    Request model for invoking a Lambda function with response streaming.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    InvocationType : str
        The invocation type.
    LogType : str
        The log type.
    ClientContext : str
        The client context.
    Qualifier : str
        Specify a version or alias to invoke a published version of the function.
    Payload : dict
        The JSON that you want to provide to your Lambda function as input.
    """

    FunctionName: constr(
        min_length=1,
        max_length=170,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_\.]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    InvocationType: Literal["RequestResponse", "DryRun"] | None = "RequestResponse"
    LogType: Literal["None", "Tail"] | None = "None"
    ClientContext: str | None
    Qualifier: (
        constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)") | None
    )
    Payload: dict | None


class InvokeWithResponseStreamResponse(BaseModel):
    """
    Response model for invoking a Lambda function with response streaming.

    Attributes
    ----------
    StatusCode : int
        The HTTP status code.
    ExecutedVersion : str
        The version of the function that executed.
    ResponseStreamContentType : str
        The type of data the stream is returning.
    InvokeComplete : InvokeComplete
        An object that's returned when the stream has ended and all the payload chunks
        have been returned.
    PayloadChunk : PayloadChunk
        A chunk of the streamed response payload.
    """

    StatusCode: int
    ExecutedVersion: constr(min_length=1, max_length=1024, pattern=r"(\$LATEST|[0-9]+)")
    ResponseStreamContentType: str | None
    InvokeComplete: InvokeWithResponseStreamCompleteEvent | None
    PayloadChunk: InvokeResponseStreamUpdate | None
