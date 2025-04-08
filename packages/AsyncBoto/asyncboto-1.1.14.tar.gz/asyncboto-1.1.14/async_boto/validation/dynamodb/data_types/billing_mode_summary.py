from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class BillingModeSummary(BaseModel):
    """
    Contains the details for the read/write capacity mode.

    Attributes
    ----------
    BillingMode : Optional[Literal["PROVISIONED", "PAY_PER_REQUEST"]]
        Controls how you are charged for read and write throughput and how you
        manage capacity.
        Valid Values: PROVISIONED, PAY_PER_REQUEST.
    LastUpdateToPayPerRequestDateTime : Optional[datetime]
        Represents the time when PAY_PER_REQUEST was last set as the read/write
        capacity mode.
    """

    BillingMode: Literal["PROVISIONED", "PAY_PER_REQUEST"] | None = None
    LastUpdateToPayPerRequestDateTime: datetime | None = None
