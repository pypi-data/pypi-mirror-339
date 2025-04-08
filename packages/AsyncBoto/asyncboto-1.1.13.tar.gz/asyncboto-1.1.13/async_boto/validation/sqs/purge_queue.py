from pydantic import BaseModel


class PurgeQueueRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    QueueUrl : str
        The URL of the queue from which the PurgeQueue action deletes messages.
    """

    QueueUrl: str


class PurgeQueueResponse(BaseModel):
    """
    The response returned in JSON format by the service.
    """

    pass
