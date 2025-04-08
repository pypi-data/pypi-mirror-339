from pydantic import BaseModel, constr

from .data_types.cors import Cors as CorsModel


class UpdateFunctionUrlConfigRequest(BaseModel):
    """
    Request model for updating the configuration for a Lambda function URL.

    Parameters
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
        The length constraint applies only to the full ARN. If you specify only the
        function name, it is limited to 64 characters in length.
    Qualifier : Optional[str]
        The alias name. Minimum length of 1. Maximum length of 128.
    AuthType : Optional[str]
        The type of authentication that your function URL uses.
        Valid values: NONE, AWS_IAM.
    Cors : Optional[Cors]
        The cross-origin resource sharing (CORS) settings for your function URL.
    InvokeMode : Optional[str]
        The invocation mode for your function URL.
        Valid values: BUFFERED, RESPONSE_STREAM.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: (
        constr(
            min_length=1,
            max_length=128,
        )
        | None
    )
    AuthType: str | None
    Cors: CorsModel | None
    InvokeMode: str | None


class UpdateFunctionUrlConfigResponse(BaseModel):
    """
    Response model for updating the configuration for a Lambda function URL.

    Parameters
    ----------
    AuthType : Optional[str]
        The type of authentication that your function URL uses.
    Cors : Optional[CorsResponse]
        The cross-origin resource sharing (CORS) settings for your function URL.
    CreationTime : Optional[str]
        When the function URL was created, in ISO-8601 format.
    FunctionArn : Optional[str]
        The Amazon Resource Name (ARN) of your function.
    FunctionUrl : Optional[str]
        The HTTP URL endpoint for your function.
    InvokeMode : Optional[str]
        The invocation mode for your function URL.
    LastModifiedTime : Optional[str]
        When the function URL configuration was last updated, in ISO-8601 format.
    """

    AuthType: str | None
    Cors: CorsModel | None
    CreationTime: str | None
    FunctionArn: str | None
    FunctionUrl: str | None
    InvokeMode: str | None
    LastModifiedTime: str | None
