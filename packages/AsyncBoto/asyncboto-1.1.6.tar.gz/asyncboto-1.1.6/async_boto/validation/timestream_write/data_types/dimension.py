from typing import Literal

from pydantic import BaseModel, constr


class Dimension(BaseModel):
    """
    Represents the metadata attributes of the time series.

    Attributes
    ----------
    Name : str
        The name of the dimension.
    Value : str
        The value of the dimension.
    DimensionValueType : str | None
        The data type of the dimension for the time-series data point.
    """

    Name: constr(min_length=1, max_length=60)
    Value: str
    DimensionValueType: Literal["VARCHAR"] | None = None
