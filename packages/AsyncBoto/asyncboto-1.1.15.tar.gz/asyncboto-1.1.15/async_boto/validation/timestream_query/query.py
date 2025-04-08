from pydantic import BaseModel, Field, constr

from .data_types.column_info import ColumnInfo
from .data_types.query_insights import QueryInsights
from .data_types.query_insights_response import QueryInsightsResponse
from .data_types.query_status import QueryStatus
from .data_types.row import Row


class QueryRequest(BaseModel):
    """
    Query is a synchronous operation that enables you to run a query against
    your Amazon Timestream data.

    Parameters
    ----------
    ClientToken : str
        Unique, case-sensitive string of up to 64 ASCII characters specified
        when a Query request is made. Providing a ClientToken makes the call
        to Query idempotent.
    MaxRows : int
        The total number of rows to be returned in the Query output.
    NextToken : str
        A pagination token used to return a set of results.
    QueryInsights : QueryInsights
        Encapsulates settings for enabling QueryInsights.
    QueryString : str
        The query to be run by Timestream.
    """

    ClientToken: constr(min_length=32, max_length=128) | None = None
    MaxRows: int | None = Field(None, ge=1, le=1000)
    NextToken: constr(min_length=1, max_length=2048) | None = None
    QueryInsights: QueryInsights | None = None
    QueryString: constr(min_length=1, max_length=262144)


class QueryResponse(BaseModel):
    """
    The response returned by the service when a Query action is successful.

    Parameters
    ----------
    ColumnInfo : List[ColumnInfo]
        The column data types of the returned result set.
    NextToken : Optional[str]
        A pagination token that can be used again on a
        Query call to get the next set of results.
    QueryId : str
        A unique ID for the given query.
    QueryInsightsResponse : Optional[QueryInsightsResponse]
        Encapsulates QueryInsights containing insights and metrics related to the query.
    QueryStatus : QueryStatus
        Information about the status of the query, including progress and bytes scanned.
    Rows : List[Row]
        The result set rows returned by the query.
    """

    ColumnInfo: list[ColumnInfo]
    NextToken: constr(min_length=1, max_length=2048) | None = None
    QueryId: constr(min_length=1, max_length=64, pattern=r"[a-zA-Z0-9]+")
    QueryInsightsResponse: QueryInsightsResponse | None = None
    QueryStatus: QueryStatus
    Rows: list[Row]
