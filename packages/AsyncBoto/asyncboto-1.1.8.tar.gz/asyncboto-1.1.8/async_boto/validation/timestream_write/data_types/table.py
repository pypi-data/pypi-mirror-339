from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr

from .magnetic_store_write_properties import MagneticStoreWriteProperties
from .retention_properties import RetentionProperties
from .schema import Schema


class Table(BaseModel):
    """
    Represents a database table in Timestream. Tables contain one or more
    related time series.
    You can modify the retention duration of the memory store and the magnetic
    store for a table.

    Attributes
    ----------
    Arn : str | None
        The Amazon Resource Name that uniquely identifies this table.
    CreationTime : datetime | None
        The time when the Timestream table was created.
    DatabaseName : str | None
        The name of the Timestream database that contains this table.
    LastUpdatedTime : datetime | None
        The time when the Timestream table was last updated.
    MagneticStoreWriteProperties : MagneticStoreWriteProperties | None
        Contains properties to set on the table when enabling magnetic store writes.
    RetentionProperties : RetentionProperties | None
        The retention duration for the memory store and magnetic store.
    Schema : Schema | None
        The schema of the table.
    TableName : str | None
        The name of the Timestream table.
    TableStatus : str | None
        The current state of the table.
    """

    Arn: str | None = None
    CreationTime: datetime | None = None
    DatabaseName: constr(min_length=3, max_length=256) | None = None
    LastUpdatedTime: datetime | None = None
    MagneticStoreWriteProperties: MagneticStoreWriteProperties | None = None
    RetentionProperties: RetentionProperties | None = None
    Schema: Schema | None = None
    TableName: constr(min_length=3, max_length=256) | None = None
    TableStatus: Literal["ACTIVE", "DELETING", "RESTORING"] | None = None
