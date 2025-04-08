from typing import Literal

from pydantic import BaseModel, constr

from .data_types.cors import Cors


class GetFunctionUrlConfigRequest(BaseModel):
    """
    Request model for retrieving details about a Lambda function URL.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    Qualifier : str
        The alias name.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: constr(
        min_length=1,
        max_length=128,
    )


class GetFunctionUrlConfigResponse(BaseModel):
    """
    Response model for retrieving details about a Lambda function URL.

    Attributes
    ----------
    AuthType : str
        The type of authentication that your function URL uses.
    Cors : Cors
        The cross-origin resource sharing (CORS) settings for your function URL.
    CreationTime : str
        When the function URL was created, in ISO-8601 format.
    FunctionArn : str
        The Amazon Resource Name (ARN) of your function.
    FunctionUrl : str
        The HTTP URL endpoint for your function.
    InvokeMode : str
        The invocation mode for your function URL.
    LastModifiedTime : str
        When the function URL configuration was last updated, in ISO-8601 format.
    """

    AuthType: Literal["NONE", "AWS_IAM"]
    Cors: Cors | None
    CreationTime: str | None
    FunctionArn: (
        constr(
            pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}(-gov)?-[a-z]+-\d{1}:\d{12}:function:[a-zA-Z0-9-_]+(:(\$LATEST|[a-zA-Z0-9-_]+))?"  # noqa: E501
        )
        | None
    )
    FunctionUrl: constr(min_length=40, max_length=100) | None
    InvokeMode: Literal["BUFFERED", "RESPONSE_STREAM"]
    LastModifiedTime: str | None
