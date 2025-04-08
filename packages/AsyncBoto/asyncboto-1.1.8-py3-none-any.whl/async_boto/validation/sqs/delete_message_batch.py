from pydantic import BaseModel

from .data_types.batch_result_error_entry import BatchResultErrorEntry
from .data_types.delete_message_batch_request_entry import (
    DeleteMessageBatchRequestEntry,
)
from .data_types.delete_message_batch_result_entry import DeleteMessageBatchResultEntry


class DeleteMessageBatchRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    Entries : List[DeleteMessageBatchRequestEntry]
        Lists the receipt handles for the messages to be deleted.
    QueueUrl : str
        The URL of the Amazon SQS queue from which messages are deleted.
    """

    Entries: list[DeleteMessageBatchRequestEntry]
    QueueUrl: str


class DeleteMessageBatchResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    Failed : List[BatchResultErrorEntry]
        A list of BatchResultErrorEntry items.
    Successful : List[DeleteMessageBatchResultEntry]
        A list of DeleteMessageBatchResultEntry items.
    """

    Failed: list[BatchResultErrorEntry]
    Successful: list[DeleteMessageBatchResultEntry]
