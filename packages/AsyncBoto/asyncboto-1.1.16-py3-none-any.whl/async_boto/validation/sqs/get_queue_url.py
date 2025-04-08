from pydantic import BaseModel, constr


class GetQueueUrlRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    QueueName : str
        The name of the queue for which you want to fetch the URL.
    QueueOwnerAWSAccountId : Optional[str]
        The AWS account ID of the account that created the queue.
    """

    QueueName: constr(max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    QueueOwnerAWSAccountId: str | None = None


class GetQueueUrlResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    QueueUrl : str
        The URL of the queue.
    """

    QueueUrl: str
