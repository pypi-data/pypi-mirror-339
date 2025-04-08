from pydantic import BaseModel


class DeleteFunctionRequest(BaseModel):
    """
    Request model for deleting a Lambda function.

    Parameters
    ----------
    FunctionName : str
        The name or ARN of the Lambda function or version.
        Name formats:
        - Function name – my-function (name-only), my-function:1 (with version)
        - Function ARN – arn:aws:lambda:us-west-2:123456789012:function:my-function
        - Partial ARN – 123456789012:function:my-function
    Qualifier : str, optional
        Specify a version to delete. You can't delete a version that an alias
        references.
    """

    # URI Request Parameters
    FunctionName: str
    Qualifier: str | None = None


class DeleteFunctionResponse(BaseModel):
    """
    Response model for deleting a Lambda function.

    The DeleteFunction operation doesn't return any data. A successful response
    returns an HTTP 204 status code with an empty HTTP body.
    """

    pass
