from pydantic import BaseModel, constr

from .data_types.table import Table


class DescribeTableRequest(BaseModel):
    """
    Returns information about the table, including the table name, database name,
    retention duration of the memory store and the magnetic store.

    Attributes
    ----------
    DatabaseName : str
        The name of the Timestream database.
    TableName : str
        The name of the Timestream table.
    """

    DatabaseName: constr(min_length=3, max_length=256)
    TableName: constr(min_length=3, max_length=256)


class DescribeTableResponse(BaseModel):
    """
    The response returned by the service when a DescribeTable action is successful.

    Attributes
    ----------
    Table : Table
        The Timestream table.
    """

    Table: Table
