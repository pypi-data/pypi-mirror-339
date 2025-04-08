from pydantic import BaseModel, conint, constr

from .data_types.destination_config import DestinationConfig


class UpdateFunctionEventInvokeConfigRequest(BaseModel):
    """
    Request model for updating the configuration for asynchronous invocation for a
    function, version, or alias.

    Parameters
    ----------
    FunctionName : str
        The name or ARN of the Lambda function, version, or alias.
        The length constraint applies only to the full ARN.
        If you specify only the function name, it is limited to 64 characters in length.
    Qualifier : Optional[str]
        A version number or alias name. Minimum length of 1. Maximum length of 128.
    DestinationConfig : Optional[DestinationConfig]
        A destination for events after they have been sent to a function for processing.
    MaximumEventAgeInSeconds : Optional[int]
        The maximum age of a request that Lambda sends to a function for processing.
        Valid range: Minimum value of 60. Maximum value of 21600.
    MaximumRetryAttempts : Optional[int]
        The maximum number of times to retry when the function returns an error.
        Valid range: Minimum value of 0. Maximum value of 2.
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


class UpdateFunctionEventInvokeConfigResponse(BaseModel):
    """
    Response model for updating the configuration for asynchronous invocation for a
    function, version, or alias.
    """

    DestinationConfig: DestinationConfig | None
    FunctionArn: str | None
    LastModified: int | None
    MaximumEventAgeInSeconds: int | None
    MaximumRetryAttempts: int | None
