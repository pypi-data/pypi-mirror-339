from pydantic import BaseModel


class DeleteMessageRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    QueueUrl : str
        The URL of the Amazon SQS queue from which messages are deleted.
    ReceiptHandle : str
        The receipt handle associated with the message to delete.
    """

    QueueUrl: str
    ReceiptHandle: str


class DeleteMessageResponse(BaseModel):
    """
    Represents an empty HTTP body for a successful DeleteMessage action response.
    """

    pass
