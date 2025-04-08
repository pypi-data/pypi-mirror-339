from pydantic import BaseModel, constr

from .data_types.magnetic_store_write_properties import MagneticStoreWriteProperties
from .data_types.retention_properties import RetentionProperties
from .data_types.schema import Schema
from .data_types.table import Table
from .data_types.tag import Tag


class CreateTableRequest(BaseModel):
    """
    Adds a new table to an existing database in your account. In an AWS account,
    table names must be at least unique within each Region if they are in the same
    database.

    Attributes
    ----------
    DatabaseName : str
        The name of the Timestream database.
    MagneticStoreWriteProperties : MagneticStoreWriteProperties | None
        Properties to set on the table when enabling magnetic store writes.
    RetentionProperties : RetentionProperties | None
        The duration for which your time-series data must be stored in the memory
        store and the magnetic store.
    Schema : Schema | None
        The schema of the table.
    TableName : str
        The name of the Timestream table.
    Tags : List[Tag] | None
        A list of key-value pairs to label the table.
    """

    DatabaseName: constr(min_length=3, max_length=256, pattern=r"[a-zA-Z0-9_.-]+")
    MagneticStoreWriteProperties: MagneticStoreWriteProperties | None = None
    RetentionProperties: RetentionProperties | None = None
    Schema: Schema | None = None
    TableName: constr(min_length=3, max_length=256, pattern=r"[a-zA-Z0-9_.-]+")
    Tags: list[Tag] | None = None


class CreateTableResponse(BaseModel):
    """
    The response returned by the service when a CreateTable action is successful.

    Attributes
    ----------
    Table : Table
        The newly created Timestream table.
    """

    Table: Table
