from pydantic import BaseModel


class CancelMessageMoveTaskRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    TaskHandle : str
        An identifier associated with a message movement task.
    """

    TaskHandle: str


class CancelMessageMoveTaskResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    ApproximateNumberOfMessagesMoved : int
        The approximate number of messages already moved to the destination queue.
    """

    ApproximateNumberOfMessagesMoved: int
