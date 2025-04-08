from pydantic import BaseModel


class WarmThroughput(BaseModel):
    """
    Provides visibility into the number of read and write operations your table or
    secondary index can instantaneously support.

    Attributes
    ----------
    ReadUnitsPerSecond : Optional[int]
        Represents the number of read operations your base table can
        instantaneously support.
    WriteUnitsPerSecond : Optional[int]
        Represents the number of write operations your base table can
        instantaneously support.
    """

    ReadUnitsPerSecond: int | None = None
    WriteUnitsPerSecond: int | None = None
