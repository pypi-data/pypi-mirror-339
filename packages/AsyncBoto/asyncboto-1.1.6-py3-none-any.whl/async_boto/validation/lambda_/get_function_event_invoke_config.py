from pydantic import BaseModel, constr

from .data_types.destination_config import DestinationConfig


class GetFunctionEventInvokeConfigRequest(BaseModel):
    """
    Request model for retrieving the configuration for asynchronous invocation for a
    function, version, or alias.

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
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)")


class GetFunctionEventInvokeConfigResponse(BaseModel):
    """
    Response model for retrieving the configuration for asynchronous invocation for a
    function, version, or alias.

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
    MaximumEventAgeInSeconds: int | None
    MaximumRetryAttempts: int | None
