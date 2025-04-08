from pydantic import BaseModel, constr


class InvokeAsyncRequest(BaseModel):
    """
    Request model for invoking a Lambda function asynchronously.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    InvokeArgs : dict
        The JSON that you want to provide to your Lambda function as input.
    """

    FunctionName: constr(
        min_length=1,
        max_length=170,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_\.]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",
    )
    InvokeArgs: dict


class InvokeAsyncResponse(BaseModel):
    """
    Response model for invoking a Lambda function asynchronously.

    Attributes
    ----------
    Status : int
        The status code.
    """

    Status: int
