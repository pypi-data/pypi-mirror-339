from pydantic import BaseModel


class DeleteFunctionCodeSigningConfigRequest(BaseModel):
    """
    Request model for deleting a function's code signing configuration.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    """

    FunctionName: str


class DeleteFunctionCodeSigningConfigResponse(BaseModel):
    """
    Response model for deleting a function's code signing configuration.

    This is an empty response model as the API returns a 204 No Content status.
    """

    pass
