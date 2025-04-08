from pydantic import BaseModel

from .type import Type


class ParameterMapping(BaseModel):
    """
    Mapping for named parameters.

    Parameters
    ----------
    Name : str
        Parameter name.
    Type : Type
        Contains the data type of a column in a query result set. The data type can be
        scalar or complex. The supported scalar data types are integers, Boolean,
        string, double, timestamp, date, time, and intervals. The supported complex data
        types are
        arrays, rows, and timeseries.
    """

    Name: str
    Type: Type
