from pydantic import BaseModel

from .message_attribute_value import MessageAttributeValue


class Message(BaseModel):
    """
    An Amazon SQS message.

    Attributes
    ----------
    Attributes : Optional[Dict[str, str]]
        A map of the attributes requested in ReceiveMessage to their respective values.
        Supported attributes:
        - ApproximateReceiveCount
        - ApproximateFirstReceiveTimestamp
        - MessageDeduplicationId
        - MessageGroupId
        - SenderId
        - SentTimestamp
        - SequenceNumber
        ApproximateFirstReceiveTimestamp and SentTimestamp are each returned as an
        integer representing the epoch time in milliseconds.
    Body : Optional[str]
        The message's contents (not URL-encoded).
    MD5OfBody : Optional[str]
        An MD5 digest of the non-URL-encoded message body string.
    MD5OfMessageAttributes : Optional[str]
        An MD5 digest of the non-URL-encoded message attribute string. You can use
        this attribute to verify that Amazon SQS received the message correctly.
        Amazon SQS URL-decodes the message before creating the MD5 digest.
    MessageAttributes : Optional[Dict[str, 'MessageAttributeValue']]
        Each message attribute consists of a Name, Type, and Value.
    MessageId : Optional[str]
        A unique identifier for the message. A MessageId is considered unique across
        all AWS accounts for an extended period of time.
    ReceiptHandle : Optional[str]
        An identifier associated with the act of receiving the message.
        A new receipt handle is returned every time you receive a message.
        When deleting a message, you provide the last received receipt handle to
        delete the message.
    """

    Attributes: dict[str, str] | None = None
    Body: str | None = None
    MD5OfBody: str | None = None
    MD5OfMessageAttributes: str | None = None
    MessageAttributes: dict[str, MessageAttributeValue] | None = None
    MessageId: str | None = None
    ReceiptHandle: str | None = None
