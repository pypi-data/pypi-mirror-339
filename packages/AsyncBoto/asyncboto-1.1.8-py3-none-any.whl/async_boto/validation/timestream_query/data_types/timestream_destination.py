from pydantic import BaseModel


class TimestreamDestination(BaseModel):
    """
    Destination for scheduled query.

    Parameters
    ----------
    DatabaseName : Optional[str], optional
        Timestream database name.
    TableName : Optional[str], optional
        Timestream table name.
    """

    DatabaseName: str | None = None
    TableName: str | None = None
