from pydantic import BaseModel, conint, constr


class PutFunctionConcurrencyRequest(BaseModel):
    """
    Request model for setting the concurrency limit of an AWS Lambda function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    ReservedConcurrentExecutions : int
        The number of simultaneous executions to reserve for the function.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",
    )
    ReservedConcurrentExecutions: conint(ge=0)


class PutFunctionConcurrencyResponse(BaseModel):
    """
    Response model for setting the concurrency limit of an AWS Lambda function.

    Attributes
    ----------
    ReservedConcurrentExecutions : int
        The number of concurrent executions that are reserved for this function.
    """

    ReservedConcurrentExecutions: int
