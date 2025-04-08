# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel

from .column_info import ColumnInfo


class Type(BaseModel):
    """
    Contains the data type of a column in a query result set. The data type can
    be scalar or complex. The supported scalar data types are integers, Boolean,
    string, double, timestamp, date, time, and intervals. The supported complex
    data types are arrays, rows, and timeseries.

    Parameters
    ----------
    ArrayColumnInfo : Optional[ColumnInfo], optional
        Indicates if the column is an array.
    RowColumnInfo : Optional[List[ColumnInfo]], optional
        Indicates if the column is a row.
    ScalarType : Optional[Literal['VARCHAR', 'BOOLEAN', 'BIGINT', 'DOUBLE', 'TIMESTAMP', 'DATE', 'TIME', 'INTERVAL_DAY_TO_SECOND', 'INTERVAL_YEAR_TO_MONTH', 'UNKNOWN', 'INTEGER']], optional
        Indicates if the column is of type string, integer, Boolean, double,
        timestamp, date, time. For more information, see Supported data types.
    TimeSeriesMeasureValueColumnInfo : Optional[ColumnInfo], optional
        Indicates if the column is a timeseries data type.
    """

    ArrayColumnInfo: ColumnInfo | None = None
    RowColumnInfo: list[ColumnInfo] | None = None
    ScalarType: (
        Literal[
            "VARCHAR",
            "BOOLEAN",
            "BIGINT",
            "DOUBLE",
            "TIMESTAMP",
            "DATE",
            "TIME",
            "INTERVAL_DAY_TO_SECOND",
            "INTERVAL_YEAR_TO_MONTH",
            "UNKNOWN",
            "INTEGER",
        ]
        | None
    ) = None
    TimeSeriesMeasureValueColumnInfo: ColumnInfo | None = None
