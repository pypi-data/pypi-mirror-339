from pydantic import BaseModel


class DeleteAliasRequest(BaseModel):
    """
    Request model for deleting a Lambda function alias.

    Parameters
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
        Name formats:
        - Function name - MyFunction
        - Function ARN - arn:aws:lambda:us-west-2:123456789012:function:MyFunction
        - Partial ARN - 123456789012:function:MyFunction
    Name : str
        The name of the alias to delete.
    """

    # URI Request Parameters
    FunctionName: str
    Name: str


class DeleteAliasResponse(BaseModel):
    """
    Response model for deleting a Lambda function alias.

    The DeleteAlias operation doesn't return any data. A successful response
    returns an HTTP 204 status code with an empty HTTP body.
    """

    pass
