from typing import Literal

from pydantic import BaseModel, Field

from .cors import Cors as CorsModel


class FunctionUrlConfig(BaseModel):
    """
    Details about a Lambda function URL configuration.

    Parameters
    ----------
    AuthType : Literal['NONE', 'AWS_IAM']
        The type of authentication used by the function URL.
    CreationTime : str
        When the function URL was created, in ISO-8601 format.
    FunctionArn : str
        The Amazon Resource Name (ARN) of the function.
    FunctionUrl : str
        The HTTP URL endpoint for the function.
    LastModifiedTime : str
        When the function URL configuration was last updated, in ISO-8601 format.
    Cors : Optional[Cors], optional
        The cross-origin resource sharing (CORS) settings for the function URL.
    InvokeMode : Optional[Literal['BUFFERED', 'RESPONSE_STREAM']], optional
        The invocation mode for the function URL.
    """

    AuthType: Literal["NONE", "AWS_IAM"]
    CreationTime: str
    FunctionArn: str
    FunctionUrl: str = Field(min_length=40, max_length=100)
    LastModifiedTime: str
    Cors: CorsModel | None = None
    InvokeMode: Literal["BUFFERED", "RESPONSE_STREAM"] | None = None
