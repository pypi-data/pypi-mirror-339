from pydantic import BaseModel

from .data_types.batch_result_error_entry import BatchResultErrorEntry
from .data_types.change_message_visibility_batch_request_entry import (
    ChangeMessageVisibilityBatchRequestEntry,
)
from .data_types.change_message_visibility_batch_result_entry import (
    ChangeMessageVisibilityBatchResultEntry,
)


class ChangeMessageVisibilityBatchRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    Entries : List[ChangeMessageVisibilityBatchRequestEntry]
        Lists the receipt handles of the messages for which the visibility
        timeout must be changed.
    QueueUrl : str
        The URL of the Amazon SQS queue whose messages' visibility is changed.
    """

    Entries: list[ChangeMessageVisibilityBatchRequestEntry]
    QueueUrl: str


class ChangeMessageVisibilityBatchResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    Failed : List[BatchResultErrorEntry]
        A list of BatchResultErrorEntry items.
    Successful : List[ChangeMessageVisibilityBatchResultEntry]
        A list of ChangeMessageVisibilityBatchResultEntry items.
    """

    Failed: list[BatchResultErrorEntry]
    Successful: list[ChangeMessageVisibilityBatchResultEntry]
