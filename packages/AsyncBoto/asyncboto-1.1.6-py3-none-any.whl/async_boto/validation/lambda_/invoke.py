from typing import Literal

from pydantic import BaseModel, constr


class InvokeRequest(BaseModel):
    """
    Request model for invoking a Lambda function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function, version, or alias.
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
    InvocationType: Literal["Event", "RequestResponse", "DryRun"] | None = (
        "RequestResponse"
    )
    LogType: Literal["None", "Tail"] | None = "None"
    ClientContext: str | None
    Qualifier: (
        constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)") | None
    )
    Payload: dict | None


class InvokeResponse(BaseModel):
    """
    Response model for invoking a Lambda function.

    Attributes
    ----------
    StatusCode : int
        The HTTP status code.
    FunctionError : str
        Indicates that an error occurred during function execution.
    LogResult : str
        The last 4 KB of the execution log, which is base64-encoded.
    ExecutedVersion : str
        The version of the function that executed.
    Payload : dict
        The response from the function, or an error object.
    """

    StatusCode: int
    FunctionError: str | None
    LogResult: str | None
    ExecutedVersion: constr(min_length=1, max_length=1024, pattern=r"(\$LATEST|[0-9]+)")
    Payload: dict | None
