# ruff: noqa: A004, A001
from pydantic import BaseModel


class EnvironmentError(BaseModel):
    """
    Error messages for environment variables that couldn't be applied to a Lambda
    function.

    This model is used when there are issues setting or accessing environment variables
    during function configuration or execution.

    Parameters
    ----------
    ErrorCode : Optional[str]
        The error code indicating the type of error that occurred with the environment
        variables.

        Possible values include:
        - "AccessDenied": The Lambda service doesn't have permission to access the
          environment variables
        - "InvalidParameter": An environment variable contains invalid characters or
          format
        - "KMSAccessDenied": Lambda couldn't access the KMS key used for encryption
        - "KMSInvalidState": The KMS key used for encryption is in an invalid state
        - "KMSDisabled": The KMS key used for encryption is disabled
        - "KMSNotFound": The KMS key specified for encryption was not found
        - "TooManyEnvironmentVariables": The environment variable count exceeds the
          limit
        - "TooLargeEnvironmentVariables": The total size of environment variables
        exceeds the limit

    Message : Optional[str]
        A descriptive error message explaining why the environment variables couldn't
        be applied.

        Contains human-readable information about the error and potentially provides
        guidance
        on how to resolve the issue.
    """

    ErrorCode: str | None = None
    Message: str | None = None
