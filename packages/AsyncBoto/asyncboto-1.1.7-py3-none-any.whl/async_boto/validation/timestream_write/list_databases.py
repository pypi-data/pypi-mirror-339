from pydantic import BaseModel, conint

from .data_types.database import Database


class ListDatabasesRequest(BaseModel):
    """
    Returns a list of your Timestream databases. Service quotas apply.

    Attributes
    ----------
    MaxResults : Optional[int]
        The total number of items to return in the output.
    NextToken : Optional[str]
        The pagination token. To resume pagination, provide the NextToken value as
        argument of a subsequent API invocation.
    """

    MaxResults: conint(ge=1, le=20) | None = None
    NextToken: str | None = None


class ListDatabasesResponse(BaseModel):
    """
    The response returned by the service when a ListDatabases action is successful.

    Attributes
    ----------
    Databases : List[Database]
        A list of database names.
    NextToken : Optional[str]
        The pagination token. This parameter is returned when the response is truncated.
    """

    Databases: list[Database]
    NextToken: str | None = None
