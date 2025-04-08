import logging
from typing import TypeVar

import boto3
from pydantic import BaseModel

from async_boto.core.base_client import BaseClient
from async_boto.core.session import AsyncAWSSession
from async_boto.validation.sqs.add_permission import (
    AddPermissionRequest,
    AddPermissionResponse,
)
from async_boto.validation.sqs.cancel_message_move_task import (
    CancelMessageMoveTaskRequest,
    CancelMessageMoveTaskResponse,
)
from async_boto.validation.sqs.change_message_visibility import (
    ChangeMessageVisibilityRequest,
    ChangeMessageVisibilityResponse,
)
from async_boto.validation.sqs.change_message_visibility_batch import (
    ChangeMessageVisibilityBatchRequest,
    ChangeMessageVisibilityBatchResponse,
)
from async_boto.validation.sqs.create_queue import (
    CreateQueueRequest,
    CreateQueueResponse,
)
from async_boto.validation.sqs.delete_message import (
    DeleteMessageRequest,
    DeleteMessageResponse,
)
from async_boto.validation.sqs.delete_message_batch import (
    DeleteMessageBatchRequest,
    DeleteMessageBatchResponse,
)
from async_boto.validation.sqs.delete_queue import (
    DeleteQueueRequest,
    DeleteQueueResponse,
)
from async_boto.validation.sqs.get_queue_attributes import (
    GetQueueAttributesRequest,
    GetQueueAttributesResponse,
)
from async_boto.validation.sqs.get_queue_url import (
    GetQueueUrlRequest,
    GetQueueUrlResponse,
)
from async_boto.validation.sqs.list_dead_letter_source_queues import (
    ListDeadLetterSourceQueuesRequest,
    ListDeadLetterSourceQueuesResponse,
)
from async_boto.validation.sqs.list_message_move_tasks import (
    ListMessageMoveTasksRequest,
    ListMessageMoveTasksResponse,
)
from async_boto.validation.sqs.list_queue_tags import (
    ListQueueTagsRequest,
    ListQueueTagsResponse,
)
from async_boto.validation.sqs.list_queues import ListQueuesRequest, ListQueuesResponse
from async_boto.validation.sqs.purge_queue import PurgeQueueRequest, PurgeQueueResponse
from async_boto.validation.sqs.receive_message import (
    ReceiveMessageRequest,
    ReceiveMessageResponse,
)
from async_boto.validation.sqs.remove_permission import (
    RemovePermissionRequest,
    RemovePermissionResponse,
)
from async_boto.validation.sqs.send_message import (
    SendMessageRequest,
    SendMessageResponse,
)
from async_boto.validation.sqs.send_message_batch import (
    SendMessageBatchRequest,
    SendMessageBatchResponse,
)
from async_boto.validation.sqs.set_queue_attributes import (
    SetQueueAttributesRequest,
    SetQueueAttributesResponse,
)
from async_boto.validation.sqs.start_message_move_task import (
    StartMessageMoveTaskRequest,
    StartMessageMoveTaskResponse,
)
from async_boto.validation.sqs.tag_queue import TagQueueRequest, TagQueueResponse
from async_boto.validation.sqs.untag_queue import UntagQueueRequest, UntagQueueResponse

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AsyncSQSClient(BaseClient):
    def __init__(self, aws_session: boto3.Session | AsyncAWSSession):
        super().__init__(aws_session=aws_session, service_name="sqs")
        self._url = f"https://sqs.{self._aws_session.region_name}.amazonaws.com"

    async def _make_request(
        self, target: str, request: BaseModel, response_cls: type[T]
    ) -> T:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
            "X-Amz-Target": target,
        }
        resp = await self._post(
            url=self._url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        print(resp.json)
        return response_cls(**resp.json)

    async def add_permission(
        self, request: AddPermissionRequest
    ) -> AddPermissionResponse:
        return await self._make_request(
            "AmazonSQS.AddPermission",
            request,
            AddPermissionResponse,
        )

    async def cancel_message_move_task(
        self, request: CancelMessageMoveTaskRequest
    ) -> CancelMessageMoveTaskResponse:
        return await self._make_request(
            "AmazonSQS.CancelMessageMoveTask",
            request,
            CancelMessageMoveTaskResponse,
        )

    async def change_message_visibility(
        self, request: ChangeMessageVisibilityRequest
    ) -> ChangeMessageVisibilityResponse:
        return await self._make_request(
            "AmazonSQS.ChangeMessageVisibility",
            request,
            ChangeMessageVisibilityResponse,
        )

    async def change_message_visibility_batch(
        self, request: ChangeMessageVisibilityBatchRequest
    ) -> ChangeMessageVisibilityBatchResponse:
        return await self._make_request(
            "AmazonSQS.ChangeMessageVisibilityBatch",
            request,
            ChangeMessageVisibilityBatchResponse,
        )

    async def create_queue(self, request: CreateQueueRequest) -> CreateQueueResponse:
        return await self._make_request(
            "AmazonSQS.CreateQueue",
            request,
            CreateQueueResponse,
        )

    async def delete_message(
        self, request: DeleteMessageRequest
    ) -> DeleteMessageResponse:
        return await self._make_request(
            "AmazonSQS.DeleteMessage",
            request,
            DeleteMessageResponse,
        )

    async def delete_message_batch(
        self, request: DeleteMessageBatchRequest
    ) -> DeleteMessageBatchResponse:
        return await self._make_request(
            "AmazonSQS.DeleteMessageBatch",
            request,
            DeleteMessageBatchResponse,
        )

    async def delete_queue(self, request: DeleteQueueRequest) -> DeleteQueueResponse:
        return await self._make_request(
            "AmazonSQS.DeleteQueue",
            request,
            DeleteQueueResponse,
        )

    async def get_queue_attributes(
        self, request: GetQueueAttributesRequest
    ) -> GetQueueAttributesResponse:
        return await self._make_request(
            "AmazonSQS.GetQueueAttributes",
            request,
            GetQueueAttributesResponse,
        )

    async def get_queue_url(self, request: GetQueueUrlRequest) -> GetQueueUrlResponse:
        return await self._make_request(
            "AmazonSQS.GetQueueUrl",
            request,
            GetQueueUrlResponse,
        )

    async def list_dead_letter_source_queues(
        self, request: ListDeadLetterSourceQueuesRequest
    ) -> ListDeadLetterSourceQueuesResponse:
        return await self._make_request(
            "AmazonSQS.ListDeadLetterSourceQueues",
            request,
            ListDeadLetterSourceQueuesResponse,
        )

    async def list_message_move_tasks(
        self, request: ListMessageMoveTasksRequest
    ) -> ListMessageMoveTasksResponse:
        return await self._make_request(
            "AmazonSQS.ListMessageMoveTasks",
            request,
            ListMessageMoveTasksResponse,
        )

    async def list_queues(self, request: ListQueuesRequest) -> ListQueuesResponse:
        return await self._make_request(
            "AmazonSQS.ListQueues",
            request,
            ListQueuesResponse,
        )

    async def list_queue_tags(
        self, request: ListQueueTagsRequest
    ) -> ListQueueTagsResponse:
        return await self._make_request(
            "AmazonSQS.ListQueueTags",
            request,
            ListQueueTagsResponse,
        )

    async def purge_queue(self, request: PurgeQueueRequest) -> PurgeQueueResponse:
        return await self._make_request(
            "AmazonSQS.PurgeQueue",
            request,
            PurgeQueueResponse,
        )

    async def receive_message(
        self, request: ReceiveMessageRequest
    ) -> ReceiveMessageResponse:
        return await self._make_request(
            "AmazonSQS.ReceiveMessage",
            request,
            ReceiveMessageResponse,
        )

    async def remove_permission(
        self, request: RemovePermissionRequest
    ) -> RemovePermissionResponse:
        return await self._make_request(
            "AmazonSQS.RemovePermission",
            request,
            RemovePermissionResponse,
        )

    async def send_message(self, request: SendMessageRequest) -> SendMessageResponse:
        return await self._make_request(
            "AmazonSQS.SendMessage",
            request,
            SendMessageResponse,
        )

    async def send_message_batch(
        self, request: SendMessageBatchRequest
    ) -> SendMessageBatchResponse:
        return await self._make_request(
            "AmazonSQS.SendMessageBatch",
            request,
            SendMessageBatchResponse,
        )

    async def set_queue_attributes(
        self, request: SetQueueAttributesRequest
    ) -> SetQueueAttributesResponse:
        return await self._make_request(
            "AmazonSQS.SetQueueAttributes",
            request,
            SetQueueAttributesResponse,
        )

    async def start_message_move_task(
        self, request: StartMessageMoveTaskRequest
    ) -> StartMessageMoveTaskResponse:
        return await self._make_request(
            "AmazonSQS.StartMessageMoveTask",
            request,
            StartMessageMoveTaskResponse,
        )

    async def tag_queue(self, request: TagQueueRequest) -> TagQueueResponse:
        return await self._make_request(
            "AmazonSQS.TagQueue",
            request,
            TagQueueResponse,
        )

    async def untag_queue(self, request: UntagQueueRequest) -> UntagQueueResponse:
        return await self._make_request(
            "AmazonSQS.UntagQueue",
            request,
            UntagQueueResponse,
        )
