from pydantic import BaseModel

from .type import Type


class ColumnInfo(BaseModel):
    """
    Contains the metadata for query results such as the column names,
    data types, and other attributes.

    Attributes
    ----------
    Type : Type
        The data type of the result set column.
        The data type can be a scalar or complex.
        Scalar data types are integers, strings, doubles, Booleans, and others.
        Complex data types are types such as arrays, rows, and others.
    Name : Optional[str]
        The name of the result set column.
        The name of the result set is available for columns
        of all data types except for arrays.
    """

    Type: Type
    Name: str | None = None
