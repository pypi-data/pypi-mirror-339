from pydantic import BaseModel


class OnFailure(BaseModel):
    """
    A destination for events that failed processing.

    Attributes
    ----------
    Destination : Optional[str]
        The Amazon Resource Name (ARN) of the destination resource.
        Supports ARNs for SNS topics, SQS queues, S3 buckets, Lambda functions,
        or EventBridge event buses for retaining records of unsuccessful asynchronous
        invocations.
    """

    Destination: str | None = None
