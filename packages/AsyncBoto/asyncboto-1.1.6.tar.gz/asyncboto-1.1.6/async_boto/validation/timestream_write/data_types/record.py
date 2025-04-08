# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, conint, constr

from .dimension import Dimension


class Record(BaseModel):
    """
    Represents a time-series data point being written into Timestream.

    Attributes
    ----------
    Dimensions : List[Dimension] | None
        The list of dimensions for time-series data points.
    MeasureName : str | None
        The name of the measure being collected.
    MeasureValue : str | None
        The measure value for the time-series data point.
    MeasureValues : List[MeasureValue] | None
        The list of measure values for time-series data points.
    MeasureValueType : str | None
        The data type of the measure value for the time-series data point.
    Time : str | None
        The time at which the measure value for the data point was collected.
    TimeUnit : str | None
        The granularity of the timestamp unit.
    Version : int | None
        The version attribute used for record updates.
    """

    Dimensions: list[Dimension] | None = None
    MeasureName: constr(min_length=1, max_length=256) | None = None
    MeasureValue: constr(min_length=1, max_length=2048) | None = None
    MeasureValues: list[MeasureValue] | None = None
    MeasureValueType: (
        Literal["DOUBLE", "BIGINT", "VARCHAR", "BOOLEAN", "TIMESTAMP", "MULTI"] | None
    ) = None
    Time: constr(min_length=1, max_length=256) | None = None
    TimeUnit: (
        Literal["MILLISECONDS", "SECONDS", "MICROSECONDS", "NANOSECONDS"] | None
    ) = None
    Version: conint(ge=1) | None = None
