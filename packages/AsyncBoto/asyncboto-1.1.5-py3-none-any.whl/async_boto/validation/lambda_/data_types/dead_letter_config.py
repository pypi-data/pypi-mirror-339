from pydantic import BaseModel


class DeadLetterConfig(BaseModel):
    """
    The dead-letter queue configuration for a Lambda function.

    A dead-letter queue is a destination for events that failed asynchronous processing.
    Lambda sends events to the dead-letter queue when they've exhausted all processing
    attempts or have expired before successful processing.

    Parameters
    ----------
    TargetArn : Optional[str]
        The Amazon Resource Name (ARN) of the destination resource for failed events.

        This can be:
        - An Amazon SQS queue ARN (arn:aws:sqs:[region]:[account-id]:[queue-name])
        - An Amazon SNS topic ARN (arn:aws:sns:[region]:[account-id]:[topic-name])

        When Lambda can't process an event (due to function errors, throttling, or
        exceeding the maximum event age), it sends the event to this destination.
        This helps prevent data loss and enables you to analyze or reprocess failed
        events.

        When not specified, failed events are discarded.
    """

    TargetArn: str | None = None
