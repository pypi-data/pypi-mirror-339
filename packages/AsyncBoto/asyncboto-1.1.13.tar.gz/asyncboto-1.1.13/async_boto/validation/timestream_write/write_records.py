from pydantic import BaseModel, constr

from .data_types.record import Record
from .data_types.records_ingested import RecordsIngested


class WriteRecordsRequest(BaseModel):
    """
    Writes a batch of records into a Timestream table.

    Attributes
    ----------
    CommonAttributes : Optional[Record]
        A record that contains the common measure, dimension, time, and version
        attributes shared across all the records in the request.
    DatabaseName : str
        The name of the Timestream database.
    Records : List[Record]
        An array of records that contain the unique measure, dimension, time,
        and version attributes for each time-series data point.
    TableName : str
        The name of the Timestream table.
    """

    CommonAttributes: Record | None
    DatabaseName: constr(min_length=3, max_length=256)
    Records: list[Record]
    TableName: constr(min_length=3, max_length=256)


class WriteRecordsResponse(BaseModel):
    """
    The response returned by the service when a WriteRecords action is successful.

    Attributes
    ----------
    RecordsIngested : RecordsIngested
        Information on the records ingested by this request.
    """

    RecordsIngested: RecordsIngested
