from pydantic import BaseModel


class OnSuccess(BaseModel):
    """
    A destination for events that were processed successfully.

    Attributes
    ----------
    Destination : Optional[str]
        The Amazon Resource Name (ARN) of the destination resource.
        Supports ARNs for SNS topics, SQS queues, Lambda functions,
        or EventBridge event buses for retaining records of successful
        asynchronous invocations.
    """

    Destination: str | None = None
