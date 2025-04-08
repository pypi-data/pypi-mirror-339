from pydantic import BaseModel, conint


class StartMessageMoveTaskRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    DestinationArn : Optional[str]
        The ARN of the queue that receives the moved messages.
    MaxNumberOfMessagesPerSecond : Optional[int]
        The number of messages to be moved per second (the message movement rate).
    SourceArn : str
        The ARN of the queue that contains the messages to be moved to another queue.
    """

    DestinationArn: str | None = None
    MaxNumberOfMessagesPerSecond: conint(ge=1, le=500) | None = None
    SourceArn: str


class StartMessageMoveTaskResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    TaskHandle : str
        An identifier associated with a message movement task.
    """

    TaskHandle: str
