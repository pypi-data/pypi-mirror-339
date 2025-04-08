from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class TableClassSummary(BaseModel):
    """
    Contains details of the table class.

    Attributes
    ----------
    LastUpdateDateTime : Optional[datetime]
        The date and time at which the table class was last updated.
    TableClass : Optional[Literal['STANDARD', 'STANDARD_INFREQUENT_ACCESS']]
        The table class of the specified table.
    """

    LastUpdateDateTime: datetime | None = None
    TableClass: Literal["STANDARD", "STANDARD_INFREQUENT_ACCESS"] | None = None
