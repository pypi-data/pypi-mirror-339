from pydantic import BaseModel, constr


class GetFunctionConcurrencyRequest(BaseModel):
    """
    Request model for retrieving details about the reserved concurrency configuration
    for a function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )


class GetFunctionConcurrencyResponse(BaseModel):
    """
    Response model for retrieving details about the reserved concurrency configuration
    for a function.

    Attributes
    ----------
    ReservedConcurrentExecutions : int
        The number of simultaneous executions that are reserved for the function.
    """

    ReservedConcurrentExecutions: int
