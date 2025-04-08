from typing import Literal

from pydantic import BaseModel, constr


class GetRuntimeManagementConfigRequest(BaseModel):
    """
    Request model for retrieving the runtime management configuration for a function's
    version.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    Qualifier : str
        Specify a version of the function.
    """

    FunctionName: constr(
        min_length=1,
        max_length=170,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_\.]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)")


class GetRuntimeManagementConfigResponse(BaseModel):
    """
    Response model for retrieving the runtime management configuration for a function's
    version.

    Attributes
    ----------
    FunctionArn : str
        The Amazon Resource Name (ARN) of your function.
    RuntimeVersionArn : str
        The ARN of the runtime the function is configured to use.
    UpdateRuntimeOn : str
        The current runtime update mode of the function.
    """

    FunctionArn: constr(
        pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}(-gov)?-[a-z]+-\d{1}:\d{12}:function:[a-zA-Z0-9-_\.]+(:(\$LATEST|[a-zA-Z0-9-_]+))?"  # noqa: E501
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
