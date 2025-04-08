from pydantic import BaseModel

from .on_failure import OnFailure as OnFailureModel
from .on_success import OnSuccess as OnSuccessModel


class DestinationConfig(BaseModel):
    """
    A configuration object that specifies the destination of an event after Lambda
    processes it.

    This configuration allows you to route both successful and failed events to other
    AWS services
    for further processing, archiving, or monitoring. It's commonly used for
    asynchronous invocations and stream-based event sources.

    Parameters
    ----------
    OnFailure : Optional[OnFailure]
        The destination configuration for failed invocations.

        Specifies where Lambda should send events that failed processing.
        For asynchronous invocations, failures occur when the function returns an error
        or when the event exceeds the maximum age or retry attempts.
        For stream-based event sources, failures occur when the function returns
        an error
        and all retry attempts are exhausted.

    OnSuccess : Optional[OnSuccess]
        The destination configuration for successful invocations.

        Specifies where Lambda should send events after they have been successfully
        processed by your Lambda function.

        Note: For stream-based event sources (Kinesis, DynamoDB, MSK, and
        self-managed Kafka),
        only the OnFailure destination is supported.
    """

    OnFailure: OnFailureModel | None = None
    OnSuccess: OnSuccessModel | None = None
