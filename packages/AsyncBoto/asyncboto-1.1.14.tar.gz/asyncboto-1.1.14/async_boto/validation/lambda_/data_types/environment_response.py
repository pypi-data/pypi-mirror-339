# ruff: noqa: A004
from pydantic import BaseModel

from .environment_error import EnvironmentError


class EnvironmentResponse(BaseModel):
    """
    The results of an operation to update or read environment variables for a Lambda
    function.

    This model is returned by Lambda API operations that interact with environment
    variables,
    such as GetFunctionConfiguration and UpdateFunctionConfiguration. It contains the
    environment variables if the operation succeeded, or error details if it failed.

    Parameters
    ----------
    Error : Optional[EnvironmentError]
        Error messages for environment variables that couldn't be applied.

        If present, indicates that there was a problem setting or retrieving
        environment variables. Contains an error code and descriptive message
        to help diagnose the issue.

        If None, the operation was successful.

    Variables : Optional[Dict[str, str]]
        Environment variable key-value pairs available to the function.

        These key-value pairs are accessible from the function's code during execution.
        For security reasons, this field is omitted from AWS CloudTrail logs to avoid
        exposing potentially sensitive information.

        Constraints:
        - Keys must start with a letter and contain only letters, numbers,
        and underscore
        - Keys are case-sensitive
    """

    Error: EnvironmentError | None = None
    Variables: dict[str, str] | None = None
