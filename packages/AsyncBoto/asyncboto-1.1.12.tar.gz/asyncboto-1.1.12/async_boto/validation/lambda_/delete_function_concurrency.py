from pydantic import BaseModel, constr


class DeleteFunctionConcurrencyRequest(BaseModel):
    """
    Request model for deleting a function's concurrency configuration.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",
    )


class DeleteFunctionConcurrencyResponse(BaseModel):
    """
    Response model for deleting a function's concurrency configuration.

    This is an empty response model as the API returns a 204 No Content status.
    """

    pass
