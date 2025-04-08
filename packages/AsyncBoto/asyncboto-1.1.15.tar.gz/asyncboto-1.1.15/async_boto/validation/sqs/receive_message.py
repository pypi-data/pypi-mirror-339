from pydantic import BaseModel, conint

from .data_types.message import Message


class ReceiveMessageRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    AttributeNames : Optional[List[str]]
        A list of attributes that need to be returned along with each message.
    MaxNumberOfMessages : Optional[int]
        The maximum number of messages to return.
    MessageAttributeNames : Optional[List[str]]
        The name of the message attribute.
    MessageSystemAttributeNames : Optional[List[str]]
        A list of attributes that need to be returned along with each message.
    QueueUrl : str
        The URL of the Amazon SQS queue from which messages are received.
    ReceiveRequestAttemptId : Optional[str]
        The token used for deduplication of ReceiveMessage calls.
    VisibilityTimeout : Optional[int]
        The duration (in seconds) that the received messages are hidden from subsequent
         retrieve requests.
    WaitTimeSeconds : Optional[int]
        The duration (in seconds) for which the call waits for a message to arrive in
        the queue before returning.
    """

    AttributeNames: list[str] | None = None
    MaxNumberOfMessages: conint(ge=1, le=10) | None = None
    MessageAttributeNames: list[str] | None = None
    MessageSystemAttributeNames: list[str] | None = None
    QueueUrl: str
    ReceiveRequestAttemptId: str | None = None
    VisibilityTimeout: int | None = None
    WaitTimeSeconds: int | None = None


class ReceiveMessageResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    Messages : List[Message]
        A list of messages received from the queue.
    """

    Messages: list[Message]
