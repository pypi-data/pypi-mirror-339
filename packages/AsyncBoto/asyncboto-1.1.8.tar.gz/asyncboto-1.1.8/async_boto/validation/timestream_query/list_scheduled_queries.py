from pydantic import BaseModel, Field

from .data_types.scheduled_query import ScheduledQuery


class ListScheduledQueriesRequest(BaseModel):
    """
    Gets a list of all scheduled queries in the caller's Amazon account and Region.
    ListScheduledQueries is eventually consistent.

    Parameters
    ----------
    MaxResults : int
        The maximum number of items to return in the output.
        If the total number of items available is more than the value specified,
        a NextToken is provided in the output.
        To resume pagination, provide the NextToken value as the argument to
        the subsequent call to ListScheduledQueriesRequest.
    NextToken : str
        A pagination token to resume pagination.
    """

    MaxResults: int | None = Field(None, ge=1, le=1000)
    NextToken: str | None = None


class ListScheduledQueriesResponse(BaseModel):
    """
    The response returned by the service when a ListScheduledQueries action is
    successful.

    Parameters
    ----------
    NextToken : str
        A token to specify where to start paginating. This is the NextToken from a
        previously truncated response.
    ScheduledQueries : List[ScheduledQuery]
        A list of scheduled queries.
    """

    NextToken: str | None = None
    ScheduledQueries: list[ScheduledQuery]
