from pydantic import BaseModel

from .runtime_version_error import RuntimeVersionError


class RuntimeVersionConfig(BaseModel):
    """
    The ARN of the runtime and any errors that occurred.

    Attributes
    ----------
    Error : Optional[RuntimeVersionError]
        Error response when Lambda is unable to retrieve the runtime version.
    RuntimeVersionArn : Optional[str]
        The ARN of the runtime version you want the function to use.
    """

    Error: RuntimeVersionError | None = None
    RuntimeVersionArn: str | None = None
