from typing import Literal

from pydantic import BaseModel, conint


class TableWarmThroughputDescription(BaseModel):
    """
    Represents the warm throughput value (in read units per second and write units per
    second) of the base table.

    Attributes
    ----------
    ReadUnitsPerSecond : Optional[conint(ge=1)]
        Represents the base table's warm throughput value in read units per second.
    Status : Optional[Literal['CREATING', 'UPDATING', 'DELETING', 'ACTIVE',
    'INACCESSIBLE_ENCRYPTION_CREDENTIALS', 'ARCHIVING', 'ARCHIVED']]
        Represents warm throughput value of the base table.
    WriteUnitsPerSecond : Optional[conint(ge=1)]
        Represents the base table's warm throughput value in write units per second.
    """

    ReadUnitsPerSecond: conint(ge=1) | None = None
    Status: (
        Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "ACTIVE",
            "INACCESSIBLE_ENCRYPTION_CREDENTIALS",
            "ARCHIVING",
            "ARCHIVED",
        ]
        | None
    ) = None  # noqa: E501
    WriteUnitsPerSecond: conint(ge=1) | None = None
