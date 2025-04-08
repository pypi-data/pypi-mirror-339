from typing import Annotated

from pydantic import BaseModel, Field


class FilterCriteriaError(BaseModel):
    """
    An object that contains details about an error related to filter criteria
    encryption.

    Parameters
    ----------
    ErrorCode : Optional[str], optional
        The AWS KMS exception that resulted from filter criteria encryption or
        decryption.
    Message : Optional[str], optional
        The error message.
    """

    ErrorCode: Annotated[
        str | None, Field(min_length=10, max_length=50, pattern=r"[A-Za-z]+Exception")
    ] = None
    Message: Annotated[
        str | None, Field(min_length=10, max_length=2048, pattern=r".*")
    ] = None
