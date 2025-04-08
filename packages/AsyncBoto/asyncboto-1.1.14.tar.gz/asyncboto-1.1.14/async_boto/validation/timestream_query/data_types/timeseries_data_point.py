from pydantic import BaseModel

from .datum import Datum


class TimeSeriesDataPoint(BaseModel):
    """
    The timeseries data type represents the values of a measure over time. A time
    series is an array of rows of timestamps and measure values, with rows sorted
    in ascending order of time. A TimeSeriesDataPoint is a single data point in
    the time series. It represents a tuple of (time, measure value) in a time series.

    Parameters
    ----------
    Time : str
        The timestamp when the measure value was collected.
    Value : Datum
        The measure value for the data point.
    """

    Time: str
    Value: Datum
