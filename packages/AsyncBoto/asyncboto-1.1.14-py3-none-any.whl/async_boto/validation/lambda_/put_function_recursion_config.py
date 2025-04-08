from typing import Literal

from pydantic import BaseModel, constr


class PutFunctionRecursionConfigRequest(BaseModel):
    """
    Request model for setting the recursive loop detection configuration of an AWS
    Lambda function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    RecursiveLoop : str
        The recursive loop detection configuration.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}((-gov)|(-iso([a-z]?)))?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)",  # noqa: E501
    )
    RecursiveLoop: Literal["Allow", "Terminate"]


class PutFunctionRecursionConfigResponse(BaseModel):
    """
    Response model for setting the recursive loop detection configuration of an
    AWS Lambda function.

    Attributes
    ----------
    RecursiveLoop : str
        The status of the recursive loop detection configuration.
    """

    RecursiveLoop: Literal["Allow", "Terminate"]
