from pydantic import BaseModel

from .timestream_destination import TimestreamDestination


class TargetDestination(BaseModel):
    """
    Destination details to write data for a target data source. Current
    supported data source is Timestream.

    Parameters
    ----------
    TimestreamDestination : Optional[TimestreamDestination], optional
        Query result destination details for Timestream data source.
    """

    TimestreamDestination: TimestreamDestination | None = None
