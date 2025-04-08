from pydantic import BaseModel

from .data_types.cors import Cors as CorsModel


class CreateFunctionUrlConfigRequest(BaseModel):
    """
    Request model for creating a Lambda function URL configuration.

    Parameters
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
        Name formats:
        - Function name – my-function
        - Function ARN – arn:aws:lambda:us-west-2:123456789012:function:my-function
        - Partial ARN – 123456789012:function:my-function
    Qualifier : str, optional
        The alias name.
    AuthType : str
        The type of authentication that the function URL uses.
        Set to AWS_IAM to restrict access to authenticated IAM users only.
        Set to NONE to bypass IAM authentication and create a public endpoint.
    Cors : Cors, optional
        The cross-origin resource sharing (CORS) settings for the function URL.
    InvokeMode : str, optional
        The invocation mode for the function URL.
        Set to BUFFERED to buffer responses (default).
        Set to RESPONSE_STREAM to stream response payloads.
    """

    # URI Request Parameters
    FunctionName: str
    Qualifier: str | None = None

    # Request Body Parameters
    AuthType: str
    Cors: CorsModel | None = None
    InvokeMode: str | None = None


class CreateFunctionUrlConfigResponse(BaseModel):
    """
    Response model for creating a Lambda function URL configuration.

    Parameters
    ----------
    AuthType : str
        The type of authentication that the function URL uses.
    Cors : Cors, optional
        The cross-origin resource sharing (CORS) settings for the function URL.
    CreationTime : str
        When the function URL was created, in ISO-8601 format.
    FunctionArn : str
        The Amazon Resource Name (ARN) of the function.
    FunctionUrl : str
        The HTTP URL endpoint for the function.
    InvokeMode : str, optional
        The invocation mode for the function URL.
    """

    AuthType: str
    CreationTime: str
    FunctionArn: str
    FunctionUrl: str
    Cors: CorsModel | None = None
    InvokeMode: str | None = None
