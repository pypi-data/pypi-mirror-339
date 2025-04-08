from typing import Literal

from pydantic import BaseModel, constr


class PartitionKey(BaseModel):
    """
    An attribute used in partitioning data in a table.

    Attributes
    ----------
    Type : str
        The type of the partition key.
    EnforcementInRecord : str | None
        The level of enforcement for the specification of a dimension key in
        ingested records.
    Name : str | None
        The name of the attribute used for a dimension key.
    """

    Type: Literal["DIMENSION", "MEASURE"]
    EnforcementInRecord: Literal["REQUIRED", "OPTIONAL"] | None = None
    Name: constr(min_length=1) | None = None
