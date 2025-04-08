from pydantic import BaseModel

from .row import Row  # Assuming you have a Row model defined in row.py
from .timeseries_data_point import (
    TimeSeriesDataPoint,
)


class Datum(BaseModel):
    """
    Datum represents a single data point in a query result.

    Attributes
    ----------
    ArrayValue : Optional[List['Datum']]
        Indicates if the data point is an array.
    NullValue : Optional[bool]
        Indicates if the data point is null.
    RowValue : Optional[Row]
        Indicates if the data point is a row.
    ScalarValue : Optional[str]
        Indicates if the data point is a scalar value such as integer,
        string, double, or Boolean.
    TimeSeriesValue : Optional[List[TimeSeriesDataPoint]]
        Indicates if the data point is a timeseries data type.
    """

    ArrayValue: list["Datum"] | None = None
    NullValue: bool | None = None
    RowValue: Row | None = None
    ScalarValue: str | None = None
    TimeSeriesValue: list[TimeSeriesDataPoint] | None = None


Datum.model_rebuild()
