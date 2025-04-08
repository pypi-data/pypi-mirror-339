from typing import Literal

from pydantic import BaseModel, constr


class TimeToLiveDescription(BaseModel):
    """
    The description of the Time to Live (TTL) status on the specified table.

    Attributes
    ----------
    AttributeName : Optional[constr(min_length=1, max_length=255)]
        The name of the TTL attribute for items in the table.
    TimeToLiveStatus : Optional[Literal['ENABLING', 'DISABLING', 'ENABLED', 'DISABLED']]
        The TTL status for the table.
    """

    AttributeName: constr(min_length=1, max_length=255) | None = None
    TimeToLiveStatus: Literal["ENABLING", "DISABLING", "ENABLED", "DISABLED"] | None = (
        None  # noqa: E501
    )
