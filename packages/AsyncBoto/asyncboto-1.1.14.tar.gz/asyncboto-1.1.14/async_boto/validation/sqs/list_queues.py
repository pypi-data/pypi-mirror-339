from pydantic import BaseModel, conint


class ListQueuesRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    MaxResults : Optional[int]
        Maximum number of results to include in the response.
    NextToken : Optional[str]
        Pagination token to request the next set of results.
    QueueNamePrefix : Optional[str]
        A string to use for filtering the list results.
    """

    MaxResults: conint(ge=1, le=1000) | None = None
    NextToken: str | None = None
    QueueNamePrefix: str | None = None


class ListQueuesResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    NextToken : Optional[str]
        Pagination token to include in the next request.
    QueueUrls : List[str]
        A list of queue URLs.
    """

    NextToken: str | None = None
    QueueUrls: list[str]
