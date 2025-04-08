from pydantic import BaseModel


class SendMessageBatchResultEntry(BaseModel):
    """
    Encloses a MessageId for a successfully-enqueued message in a SendMessageBatch.

    Attributes
    ----------
    Id : str
        An identifier for the message in this batch.
    MD5OfMessageBody : str
        An MD5 digest of the non-URL-encoded message body string.
    MessageId : str
        An identifier for the message.
    MD5OfMessageAttributes : Optional[str]
        An MD5 digest of the non-URL-encoded message attribute string.
    MD5OfMessageSystemAttributes : Optional[str]
        An MD5 digest of the non-URL-encoded message system attribute string.
    SequenceNumber : Optional[str]
        The large, non-consecutive number that Amazon SQS assigns to each message.
    """

    Id: str
    MD5OfMessageBody: str
    MessageId: str
    MD5OfMessageAttributes: str | None = None
    MD5OfMessageSystemAttributes: str | None = None
    SequenceNumber: str | None = None
