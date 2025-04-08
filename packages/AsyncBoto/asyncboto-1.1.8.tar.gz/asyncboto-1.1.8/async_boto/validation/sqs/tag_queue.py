from pydantic import BaseModel


class TagQueueRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    QueueUrl : str
        The URL of the queue.
    Tags : Dict[str, str]
        The list of tags to be added to the specified queue.
    """

    QueueUrl: str
    Tags: dict[str, str]


class TagQueueResponse(BaseModel):
    """
    The response returned in JSON format by the service.
    """

    pass
