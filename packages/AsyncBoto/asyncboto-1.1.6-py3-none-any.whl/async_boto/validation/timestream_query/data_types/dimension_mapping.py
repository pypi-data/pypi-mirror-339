from typing import Literal

from pydantic import BaseModel


class DimensionMapping(BaseModel):
    """
    This type is used to map column(s) from the query result to a dimension in the
    destination table.

    Attributes
    ----------
    DimensionValueType : Literal['VARCHAR']
        Type for the dimension.
    Name : str
        Column name from query result.
    """

    DimensionValueType: Literal["VARCHAR"]
    Name: str
