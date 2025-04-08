from typing import Literal

from pydantic import BaseModel, constr


class MeasureValue(BaseModel):
    """
    Represents the data attribute of the time series.

    Attributes
    ----------
    Name : str
        The name of the MeasureValue.
    Type : str
        The data type of the MeasureValue for the time-series data point.
    Value : str
        The value for the MeasureValue.
    """

    Name: constr(min_length=1)
    Type: Literal["DOUBLE", "BIGINT", "VARCHAR", "BOOLEAN", "TIMESTAMP", "MULTI"]
    Value: constr(min_length=1, max_length=2048)
