from pydantic import BaseModel, constr

from .data_types.database import Database


class DescribeDatabaseRequest(BaseModel):
    """
    Returns information about the database, including the database name,
    time that the database was created, and the total number of tables found
    within the database.

    Attributes
    ----------
    DatabaseName : str
        The name of the Timestream database.
    """

    DatabaseName: constr(min_length=3, max_length=256)


class DescribeDatabaseResponse(BaseModel):
    """
    The response returned by the service when a DescribeDatabase action is successful.

    Attributes
    ----------
    Database : Database
        The name of the Timestream table.
    """

    Database: Database
