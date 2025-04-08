from pydantic import BaseModel, conint, constr

from .data_types.table import Table


class ListTablesRequest(BaseModel):
    """
    Provides a list of tables, along with the name, status, and retention properties
    of each table.

    Attributes
    ----------
    DatabaseName : Optional[str]
        The name of the Timestream database.
    MaxResults : Optional[int]
        The total number of items to return in the output.
    NextToken : Optional[str]
        The pagination token. To resume pagination, provide the NextToken value as
        argument of a subsequent API invocation.
    """

    DatabaseName: constr(min_length=3, max_length=256) | None = None
    MaxResults: conint(ge=1, le=20) | None = None
    NextToken: str | None = None


class ListTablesResponse(BaseModel):
    """
    The response returned by the service when a ListTables action is successful.

    Attributes
    ----------
    NextToken : Optional[str]
        A token to specify where to start paginating.
        This is the NextToken from a previously truncated response.
    Tables : List[Table]
        A list of tables.
    """

    NextToken: str | None = None
    Tables: list[Table]
