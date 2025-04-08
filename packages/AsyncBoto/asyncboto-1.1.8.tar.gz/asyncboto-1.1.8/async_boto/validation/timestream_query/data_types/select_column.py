from pydantic import BaseModel

from .type import Type


class SelectColumn(BaseModel):
    """
    Details of the column that is returned by the query.

    Parameters
    ----------
    Aliased : Optional[bool], optional
        True, if the column name was aliased by the query. False otherwise.
    DatabaseName : Optional[str], optional
        Database that has this column.
    Name : Optional[str], optional
        Name of the column.
    TableName : Optional[str], optional
        Table within the database that has this column.
    Type : Optional[Type], optional
        Contains the data type of a column in a query result set. The data type can
        be scalar or complex. The supported scalar data types are integers, Boolean,
        string, double, timestamp, date, time, and intervals. The supported complex
        data types are arrays, rows, and timeseries.
    """

    Aliased: bool | None = None
    DatabaseName: str | None = None
    Name: str | None = None
    TableName: str | None = None
    Type: Type | None = None
