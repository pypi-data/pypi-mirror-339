from typing import Literal

from pydantic import BaseModel


class LastUpdate(BaseModel):
    """
    Configuration object that contains the most recent account settings update,
    visible only if settings have been updated previously.

    Parameters
    ----------
    Status : Optional[str]
        The status of the last update.
        Can be either `PENDING`, `FAILED`, or `SUCCEEDED`.
    StatusMessage : Optional[str]
        Error message describing the last account settings update status,
        visible only if an error occurred.
    TargetQueryTCU : Optional[int]
        The number of TimeStream Compute Units (TCUs) requested in the last account
        settings update.
    """

    Status: Literal["PENDING", "FAILED", "SUCCEEDED"] | None = None
    StatusMessage: str | None = None
    TargetQueryTCU: int | None = None
