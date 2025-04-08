from pydantic import BaseModel


class Capacity(BaseModel):
    """
    Represents the amount of provisioned throughput capacity consumed on a table or
     an index.

    Attributes
    ----------
    CapacityUnits : Optional[float]
        The total number of capacity units consumed on a table or an index.
    ReadCapacityUnits : Optional[float]
        The total number of read capacity units consumed on a table or an index.
    WriteCapacityUnits : Optional[float]
        The total number of write capacity units consumed on a table or an index.
    """

    CapacityUnits: float | None = None
    ReadCapacityUnits: float | None = None
    WriteCapacityUnits: float | None = None
