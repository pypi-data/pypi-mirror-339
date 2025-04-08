from pydantic import BaseModel


class ListMessageMoveTasksResultEntry(BaseModel):
    """
    Contains the details of a message movement task.

    Attributes
    ----------
    ApproximateNumberOfMessagesMoved : Optional[int]
        The approximate number of messages already moved to the destination queue.
    ApproximateNumberOfMessagesToMove : Optional[int]
        The number of messages to be moved from the source queue. This number is
        obtained at the time of starting the message movement task and is only
        included after the message movement task is selected to start.
    DestinationArn : Optional[str]
        The ARN of the destination queue if it has been specified in the
        StartMessageMoveTask request. If a DestinationArn has not been specified
        in the StartMessageMoveTask request, this field value will be NULL.
    FailureReason : Optional[str]
        The task failure reason (only included if the task status is FAILED).
    MaxNumberOfMessagesPerSecond : Optional[int]
        The number of messages to be moved per second (the message movement rate),
        if it has been specified in the StartMessageMoveTask request. If a
        MaxNumberOfMessagesPerSecond has not been specified in the StartMessageMoveTask
        request, this field value will be NULL.
    SourceArn : Optional[str]
        The ARN of the queue that contains the messages to be moved to another queue.
    StartedTimestamp : Optional[int]
        The timestamp of starting the message movement task.
    Status : Optional[str]
        The status of the message movement task. Possible values are:
        RUNNING, COMPLETED, CANCELLING, CANCELLED, and FAILED.
    TaskHandle : Optional[str]
        An identifier associated with a message movement task. When this field is
        returned in the response of the ListMessageMoveTasks action, it
        is only populated for tasks that are in RUNNING status.
    """

    ApproximateNumberOfMessagesMoved: int | None = None
    ApproximateNumberOfMessagesToMove: int | None = None
    DestinationArn: str | None = None
    FailureReason: str | None = None
    MaxNumberOfMessagesPerSecond: int | None = None
    SourceArn: str | None = None
    StartedTimestamp: int | None = None
    Status: str | None = None
    TaskHandle: str | None = None
