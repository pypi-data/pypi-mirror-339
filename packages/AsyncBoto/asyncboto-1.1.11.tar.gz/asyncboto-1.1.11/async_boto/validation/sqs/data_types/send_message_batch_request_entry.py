from pydantic import BaseModel, constr

from .message_attribute_value import MessageAttributeValue
from .message_system_attribute_value import MessageSystemAttributeValue


class SendMessageBatchRequestEntry(BaseModel):
    """
    Contains the details of a single Amazon SQS message along with an Id.

    Attributes
    ----------
    Id : str
        An identifier for a message in this batch used to communicate the result.
    MessageBody : str
        The body of the message.
    DelaySeconds : Optional[int]
        The length of time, in seconds, for which a specific message is delayed.
    MessageAttributes : Optional[Dict[str, MessageAttributeValue]]
        Each message attribute consists of a Name, Type, and Value.
    MessageDeduplicationId : Optional[str]
        The token used for deduplication of messages within a 5-minute minimum
        deduplication interval.
    MessageGroupId : Optional[str]
        The tag that specifies that a message belongs to a specific message group.
    MessageSystemAttributes : Optional[Dict[str, MessageSystemAttributeValue]]
        The message system attribute to send.
    """

    Id: constr(max_length=80, pattern=r"^[a-zA-Z0-9-_]+$")
    MessageBody: str
    DelaySeconds: int | None = None
    MessageAttributes: dict[str, MessageAttributeValue] | None = None
    MessageDeduplicationId: (
        constr(
            max_length=128, pattern=r'^[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]+$'
        )
        | None
    ) = None  # noqa: E501
    MessageGroupId: (
        constr(
            max_length=128, pattern=r'^[a-zA-Z0-9!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~]+$'
        )
        | None
    ) = None  # noqa: E501
    MessageSystemAttributes: dict[str, MessageSystemAttributeValue] | None = None
