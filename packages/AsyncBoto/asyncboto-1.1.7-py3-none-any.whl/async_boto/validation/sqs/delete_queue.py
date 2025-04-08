from pydantic import BaseModel


class DeleteQueueRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    QueueUrl : str
        The URL of the Amazon SQS queue to delete.
    """

    QueueUrl: str


class DeleteQueueResponse(BaseModel):
    """
    Represents an empty HTTP body for a successful DeleteQueue action response.
    """

    pass
