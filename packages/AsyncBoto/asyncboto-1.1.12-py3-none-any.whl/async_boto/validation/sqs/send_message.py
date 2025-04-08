from pydantic import BaseModel, conint

from .data_types.message_attribute_value import MessageAttributeValue
from .data_types.message_system_attribute_value import MessageSystemAttributeValue


class SendMessageRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    DelaySeconds : Optional[int]
        The length of time, in seconds, for which to delay a specific message.
    MessageAttributes : Optional[Dict[str, MessageAttributeValue]]
        Each message attribute consists of a Name, Type, and Value.
    MessageBody : str
        The message to send.
    MessageDeduplicationId : Optional[str]
        The token used for deduplication of sent messages.
    MessageGroupId : Optional[str]
        The tag that specifies that a message belongs to a specific message group.
    MessageSystemAttributes : Optional[Dict[str, MessageSystemAttributeValue]]
        The message system attribute to send.
    QueueUrl : str
        The URL of the Amazon SQS queue to which a message is sent.
    """

    DelaySeconds: conint(ge=0, le=900) | None = None
    MessageAttributes: dict[str, MessageAttributeValue] | None = None
    MessageBody: str
    MessageDeduplicationId: str | None = None
    MessageGroupId: str | None = None
    MessageSystemAttributes: dict[str, MessageSystemAttributeValue] | None = None
    QueueUrl: str


class SendMessageResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    MD5OfMessageAttributes : Optional[str]
        An MD5 digest of the non-URL-encoded message attribute string.
    MD5OfMessageBody : str
        An MD5 digest of the non-URL-encoded message body string.
    MD5OfMessageSystemAttributes : Optional[str]
        An MD5 digest of the non-URL-encoded message system attribute string.
    MessageId : str
        An attribute containing the MessageId of the message sent to the queue.
    SequenceNumber : Optional[str]
        The large, non-consecutive number that Amazon SQS assigns to each message.
    """

    MD5OfMessageAttributes: str | None = None
    MD5OfMessageBody: str
    MD5OfMessageSystemAttributes: str | None = None
    MessageId: str
    SequenceNumber: str | None = None
