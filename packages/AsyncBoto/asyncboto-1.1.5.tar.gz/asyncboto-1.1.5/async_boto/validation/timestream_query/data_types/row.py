from pydantic import BaseModel

from .datum import Datum


class Row(BaseModel):
    """
    Represents a single row in the query results.

    Parameters
    ----------
    Data : List[Datum]
        List of data points in a single row of the result set.
    """

    Data: list[Datum]
