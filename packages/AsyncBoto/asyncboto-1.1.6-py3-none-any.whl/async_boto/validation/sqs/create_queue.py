from typing import Literal

from pydantic import BaseModel, conint, constr


class QueueAttributes(BaseModel):
    """
    Represents the attributes for creating an SQS queue.

    Attributes
    ----------
    DelaySeconds : Optional[int]
        The length of time, in seconds, for which the delivery of all messages in the
        queue is delayed.
    MaximumMessageSize : Optional[int]
        The limit of how many bytes a message can contain before Amazon SQS rejects it.
    MessageRetentionPeriod : Optional[int]
        The length of time, in seconds, for which Amazon SQS retains a message.
    Policy : Optional[str]
        The queue's policy.
    ReceiveMessageWaitTimeSeconds : Optional[int]
        The length of time, in seconds, for which a ReceiveMessage action waits for a
        message to arrive.
    VisibilityTimeout : Optional[int]
        The visibility timeout for the queue, in seconds.
    RedrivePolicy : Optional[str]
        The string that includes the parameters for the dead-letter queue functionality
        of the source queue.
    RedriveAllowPolicy : Optional[str]
        The string that includes the parameters for the permissions for the dead-letter
        queue redrive permission.
    KmsMasterKeyId : Optional[str]
        The ID of an AWS managed customer master key (CMK) for Amazon SQS or a custom
        CMK.
    KmsDataKeyReusePeriodSeconds : Optional[int]
        The length of time, in seconds, for which Amazon SQS can reuse a data key to
        encrypt or decrypt messages before calling AWS KMS again.
    SqsManagedSseEnabled : Optional[bool]
        Enables server-side queue encryption using SQS owned encryption keys.
    FifoQueue : Optional[bool]
        Designates a queue as FIFO.
    ContentBasedDeduplication : Optional[bool]
        Enables content-based deduplication.
    DeduplicationScope : Optional[Literal['messageGroup', 'queue']]
        Specifies whether message deduplication occurs at the message group or queue
        level.
    FifoThroughputLimit : Optional[Literal['perQueue', 'perMessageGroupId']]
        Specifies whether the FIFO queue throughput quota applies to the entire queue
        or per message group.
    """

    DelaySeconds: conint(ge=0, le=900) | None = 0
    MaximumMessageSize: conint(ge=1024, le=262144) | None = 262144
    MessageRetentionPeriod: conint(ge=60, le=1209600) | None = 345600
    Policy: str | None = None
    ReceiveMessageWaitTimeSeconds: conint(ge=0, le=20) | None = 0
    VisibilityTimeout: conint(ge=0, le=43200) | None = 30
    RedrivePolicy: str | None = None
    RedriveAllowPolicy: str | None = None
    KmsMasterKeyId: str | None = None
    KmsDataKeyReusePeriodSeconds: conint(ge=60, le=86400) | None = 300
    SqsManagedSseEnabled: bool | None = None
    FifoQueue: bool | None = None
    ContentBasedDeduplication: bool | None = None
    DeduplicationScope: Literal["messageGroup", "queue"] | None = None
    FifoThroughputLimit: Literal["perQueue", "perMessageGroupId"] | None = None


class CreateQueueRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    QueueName : str
        The name of the new queue.
    Attributes : Optional[QueueAttributes]
        A map of attributes with their corresponding values.
    tags : Optional[Dict[str, str]]
        Add cost allocation tags to the specified Amazon SQS queue.
    """

    QueueName: constr(max_length=80, pattern=r"^[a-zA-Z0-9_-]+(\.fifo)?$")
    Attributes: QueueAttributes | None = None
    tags: dict[str, str] | None = None


class CreateQueueResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    QueueUrl : str
        The URL of the created Amazon SQS queue.
    """

    QueueUrl: str
