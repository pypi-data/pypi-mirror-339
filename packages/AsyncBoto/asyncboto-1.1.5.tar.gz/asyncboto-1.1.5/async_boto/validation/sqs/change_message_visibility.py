from pydantic import BaseModel, conint


class ChangeMessageVisibilityRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    QueueUrl : str
        The URL of the Amazon SQS queue whose message's visibility is changed.
    ReceiptHandle : str
        The receipt handle associated with the message, whose visibility timeout
        is changed.
    VisibilityTimeout : int
        The new value for the message's visibility timeout (in seconds).
    """

    QueueUrl: str
    ReceiptHandle: str
    VisibilityTimeout: conint(ge=0, le=43200)


class ChangeMessageVisibilityResponse(BaseModel):
    """
    Represents an empty HTTP body for a successful ChangeMessageVisibility
    action response.
    """

    pass
