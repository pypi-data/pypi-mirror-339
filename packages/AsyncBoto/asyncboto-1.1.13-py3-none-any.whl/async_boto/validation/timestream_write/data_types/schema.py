from pydantic import BaseModel

from .partition_key import PartitionKey


class Schema(BaseModel):
    """
    A Schema specifies the expected data model of the table.

    Attributes
    ----------
    CompositePartitionKey : List[PartitionKey] | None
        A non-empty list of partition keys defining the attributes used to
        partition the table data.
    """

    CompositePartitionKey: list[PartitionKey] = None
