from pydantic import BaseModel, conint, constr

from .data_types.destination_config import DestinationConfig


class PutFunctionEventInvokeConfigRequest(BaseModel):
    """
    Request model for configuring options for asynchronous invocation on an AWS
    Lambda function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function, version, or alias.
    Qualifier : str
        A version number or alias name.
    DestinationConfig : DestinationConfig
        A destination for events after they have been sent to a function for processing.
    MaximumEventAgeInSeconds : int
        The maximum age of a request that Lambda sends to a function for processing.
    MaximumRetryAttempts : int
        The maximum number of times to retry when the function returns an error.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: (
        constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)") | None
    )
    DestinationConfig: DestinationConfig | None
    MaximumEventAgeInSeconds: conint(ge=60, le=21600) | None
    MaximumRetryAttempts: conint(ge=0, le=2) | None


class PutFunctionEventInvokeConfigResponse(BaseModel):
    """
    Response model for configuring options for asynchronous invocation on an AWS
    Lambda function.

    Attributes
    ----------
    DestinationConfig : DestinationConfig
        A destination for events after they have been sent to a function for processing.
    FunctionArn : str
        The Amazon Resource Name (ARN) of the function.
    LastModified : int
        The date and time that the configuration was last updated, in Unix time seconds.
    MaximumEventAgeInSeconds : int
        The maximum age of a request that Lambda sends to a function for processing.
    MaximumRetryAttempts : int
        The maximum number of times to retry when the function returns an error.
    """

    DestinationConfig: DestinationConfig | None
    FunctionArn: (
        constr(
            pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}(-gov)?-[a-z]+-\d{1}:\d{12}:function:[a-zA-Z0-9-_]+(:(\$LATEST|[a-zA-Z0-9-_]+))?"  # noqa: E501
        )
        | None
    )
    LastModified: int | None
    MaximumEventAgeInSeconds: conint(ge=60, le=21600) | None
    MaximumRetryAttempts: conint(ge=0, le=2) | None
