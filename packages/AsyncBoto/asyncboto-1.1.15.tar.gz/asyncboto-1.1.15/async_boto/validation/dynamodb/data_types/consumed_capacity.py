# ruff: noqa: E501
from pydantic import BaseModel, constr

from .capacity import Capacity


class ConsumedCapacity(BaseModel):
    """
    The capacity units consumed by an operation. The data returned includes the total
    provisioned throughput consumed, along with statistics for the table and any indexes
    involved in the operation.

    Attributes
    ----------
    CapacityUnits : Optional[float]
        The total number of capacity units consumed by the operation.
    GlobalSecondaryIndexes : Optional[Dict[constr(min_length=3, max_length=255, regex=r"[a-zA-Z0-9_.-]+"), Capacity]]
        The amount of throughput consumed on each global index affected by the operation.
    LocalSecondaryIndexes : Optional[Dict[constr(min_length=3, max_length=255, regex=r"[a-zA-Z0-9_.-]+"), Capacity]]
        The amount of throughput consumed on each local index affected by the operation.
    ReadCapacityUnits : Optional[float]
        The total number of read capacity units consumed by the operation.
    Table : Optional[Capacity]
        The amount of throughput consumed on the table affected by the operation.
    TableName : Optional[constr(min_length=1, max_length=1024)]
        The name of the table that was affected by the operation.
    WriteCapacityUnits : Optional[float]
        The total number of write capacity units consumed by the operation.
    """

    CapacityUnits: float | None = None
    GlobalSecondaryIndexes: (
        dict[constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+"), Capacity]
        | None
    ) = None
    LocalSecondaryIndexes: (
        dict[constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+"), Capacity]
        | None
    ) = None
    ReadCapacityUnits: float | None = None
    Table: Capacity | None = None
    TableName: constr(min_length=1, max_length=1024) | None = None
    WriteCapacityUnits: float | None = None
