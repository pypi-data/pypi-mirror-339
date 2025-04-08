from typing import Literal

from pydantic import BaseModel, constr


class GetFunctionRecursionConfigRequest(BaseModel):
    """
    Request model for retrieving the recursive loop detection configuration of a
    Lambda function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}((-gov)|(-iso([a-z]?)))?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)",  # noqa: E501
    )


class GetFunctionRecursionConfigResponse(BaseModel):
    """
    Response model for retrieving the recursive loop detection configuration of a
    Lambda function.

    Attributes
    ----------
    RecursiveLoop : str
        The recursive loop detection configuration of the function.
    """

    RecursiveLoop: Literal["Allow", "Terminate"]
