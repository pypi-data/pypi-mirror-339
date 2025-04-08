from pydantic import BaseModel


class ListQueueTagsRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    QueueUrl : str
        The URL of the queue.
    """

    QueueUrl: str


class ListQueueTagsResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    Tags : Dict[str, str]
        The list of all tags added to the specified queue.
    """

    Tags: dict[str, str]
