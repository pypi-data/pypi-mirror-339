from pydantic import BaseModel, constr

from .data_types.magnetic_store_write_properties import MagneticStoreWriteProperties
from .data_types.retention_properties import RetentionProperties
from .data_types.schema import Schema
from .data_types.table import Table


class UpdateTableRequest(BaseModel):
    """
    Modifies the retention duration of the memory store and magnetic store for a
    Timestream table.

    Attributes
    ----------
    DatabaseName : str
        The name of the Timestream database.
    MagneticStoreWriteProperties : Optional[MagneticStoreWriteProperties]
        Contains properties to set on the table when enabling magnetic store writes.
    RetentionProperties : Optional[RetentionProperties]
        The retention duration of the memory store and the magnetic store.
    Schema : Optional[Schema]
        The schema of the table.
    TableName : str
        The name of the Timestream table.
    """

    DatabaseName: constr(min_length=3, max_length=256)
    MagneticStoreWriteProperties: MagneticStoreWriteProperties | None
    RetentionProperties: RetentionProperties | None
    Schema: Schema | None
    TableName: constr(min_length=3, max_length=256)


class UpdateTableResponse(BaseModel):
    """
    The response returned by the service when an UpdateTable action is successful.

    Attributes
    ----------
    Table : Table
        A top-level container for a table. Databases and tables are the fundamental
        management concepts in Amazon Timestream.
    """

    Table: Table
