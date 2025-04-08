from typing import Literal

from pydantic import BaseModel, conint


class GlobalSecondaryIndexWarmThroughputDescription(BaseModel):
    """
    The description of the warm throughput value on a global secondary index.

    Attributes
    ----------
    ReadUnitsPerSecond : Optional[conint(ge=1)]
        Represents warm throughput read units per second value for a global
        secondary index.
    Status : Optional[Literal['CREATING', 'UPDATING', 'DELETING', 'ACTIVE']]
        Represents the warm throughput status being created or updated on a global
        secondary index.
    WriteUnitsPerSecond : Optional[conint(ge=1)]
        Represents warm throughput write units per second value for a global secondary
        index.
    """

    ReadUnitsPerSecond: conint(ge=1) | None = None
    Status: Literal["CREATING", "UPDATING", "DELETING", "ACTIVE"] | None = None
    WriteUnitsPerSecond: conint(ge=1) | None = None
