from typing import Literal

from pydantic import BaseModel, constr


class PutRuntimeManagementConfigRequest(BaseModel):
    """
    Request model for setting the runtime management configuration of an AWS Lambda
    function's version.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    Qualifier : str
        The version number or alias name.
    RuntimeVersionArn : str
        The ARN of the runtime version you want the function to use.
    UpdateRuntimeOn : str
        The runtime update mode.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: (
        constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)") | None
    )
    RuntimeVersionArn: (
        constr(
            min_length=26,
            max_length=2048,
            pattern=r"^arn:(aws[a-zA-Z-]*):lambda:[a-z]{2}((-gov)|(-iso(b?)))?-[a-z]+-\d{1}::runtime:.+$",  # noqa: E501
        )
        | None
    )
    UpdateRuntimeOn: Literal["Auto", "Manual", "FunctionUpdate"]


class PutRuntimeManagementConfigResponse(BaseModel):
    """
    Response model for setting the runtime management configuration of an AWS Lambda
    function's version.

    Attributes
    ----------
    FunctionArn : str
        The ARN of the function.
    RuntimeVersionArn : str
        The ARN of the runtime the function is configured to use.
    UpdateRuntimeOn : str
        The runtime update mode.
    """

    FunctionArn: constr(
        pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}(-gov)?-[a-z]+-\d{1}:\d{12}:function:[a-zA-Z0-9-_]+(:(\$LATEST|[a-zA-Z0-9-_]+))?"  # noqa: E501
    )
    RuntimeVersionArn: (
        constr(
            min_length=26,
            max_length=2048,
            pattern=r"^arn:(aws[a-zA-Z-]*):lambda:[a-z]{2}((-gov)|(-iso(b?)))?-[a-z]+-\d{1}::runtime:.+$",  # noqa: E501
        )
        | None
    )
    UpdateRuntimeOn: Literal["Auto", "Manual", "FunctionUpdate"]
