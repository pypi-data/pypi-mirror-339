from pydantic import BaseModel

from .data_types.batch_result_error_entry import BatchResultErrorEntry
from .data_types.send_message_batch_request_entry import SendMessageBatchRequestEntry
from .data_types.send_message_batch_result_entry import SendMessageBatchResultEntry


class SendMessageBatchRequest(BaseModel):
    QueueUrl: str
    Entries: list[SendMessageBatchRequestEntry]


class SendMessageBatchResponse(BaseModel):
    Successful: list[SendMessageBatchResultEntry]
    Failed: list[BatchResultErrorEntry]
