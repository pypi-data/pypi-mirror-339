from pydantic import BaseModel, conint


class ListDeadLetterSourceQueuesRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    MaxResults : Optional[int]
        Maximum number of results to include in the response.
    NextToken : Optional[str]
        Pagination token to request the next set of results.
    QueueUrl : str
        The URL of a dead-letter queue.
    """

    MaxResults: conint(ge=1, le=1000) | None = None
    NextToken: str | None = None
    QueueUrl: str


class ListDeadLetterSourceQueuesResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    NextToken : Optional[str]
        Pagination token to include in the next request.
    queueUrls : List[str]
        A list of source queue URLs that have the RedrivePolicy queue attribute
        configured with a dead-letter queue.
    """

    NextToken: str | None = None
    queueUrls: list[str]  # noqa: N815
