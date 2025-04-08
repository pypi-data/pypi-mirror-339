from pydantic import BaseModel


class FailureException(BaseModel):
    """
    Represents a failure in a contributor insights operation.

    Attributes
    ----------
    ExceptionDescription : Optional[str]
        Description of the failure.
    ExceptionName : Optional[str]
        Exception name.
    """

    ExceptionDescription: str | None = None
    ExceptionName: str | None = None
