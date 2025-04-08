from pydantic import BaseModel


class UntagQueueRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    QueueUrl : str
        The URL of the queue.
    TagKeys : List[str]
        The list of tags to be removed from the specified queue.
    """

    QueueUrl: str
    TagKeys: list[str]


class UntagQueueResponse(BaseModel):
    """
    The response returned in JSON format by the service.
    """

    pass
