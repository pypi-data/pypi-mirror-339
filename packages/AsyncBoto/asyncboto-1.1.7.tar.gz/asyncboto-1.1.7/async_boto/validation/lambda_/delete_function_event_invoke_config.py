from pydantic import BaseModel, constr


class DeleteFunctionEventInvokeConfigRequest(BaseModel):
    """
    Request model for deleting a function's event invoke configuration.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function, version, or alias.
    Qualifier : str
        A version number or alias name.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",
    )
    Qualifier: constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)")


class DeleteFunctionEventInvokeConfigResponse(BaseModel):
    """
    Response model for deleting a function's event invoke configuration.

    This is an empty response model as the API returns a 204 No Content status.
    """

    pass
