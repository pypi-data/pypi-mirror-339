import logging
import random
from typing import TypeVar

import boto3
from pydantic import BaseModel

from async_boto.core.base_client import BaseClient
from async_boto.core.session import AsyncAWSSession
from async_boto.validation.timestream_write.create_batch_load_task import (
    CreateBatchLoadTaskRequest,
    CreateBatchLoadTaskResponse,
)
from async_boto.validation.timestream_write.create_database import (
    CreateDatabaseRequest,
    CreateDatabaseResponse,
)
from async_boto.validation.timestream_write.create_table import (
    CreateTableRequest,
    CreateTableResponse,
)
from async_boto.validation.timestream_write.delete_database import (
    DeleteDatabaseRequest,
    DeleteDatabaseResponse,
)
from async_boto.validation.timestream_write.delete_table import (
    DeleteTableRequest,
    DeleteTableResponse,
)
from async_boto.validation.timestream_write.describe_batch_load_task import (
    DescribeBatchLoadTaskRequest,
    DescribeBatchLoadTaskResponse,
)
from async_boto.validation.timestream_write.describe_database import (
    DescribeDatabaseRequest,
    DescribeDatabaseResponse,
)
from async_boto.validation.timestream_write.describe_endpoints import (
    DescribeEndpointsResponse,
)
from async_boto.validation.timestream_write.describe_table import (
    DescribeTableRequest,
    DescribeTableResponse,
)
from async_boto.validation.timestream_write.list_batch_load_tasks import (
    ListBatchLoadTasksRequest,
    ListBatchLoadTasksResponse,
)
from async_boto.validation.timestream_write.list_databases import (
    ListDatabasesRequest,
    ListDatabasesResponse,
)
from async_boto.validation.timestream_write.list_tables import (
    ListTablesRequest,
    ListTablesResponse,
)
from async_boto.validation.timestream_write.list_tags_for_resource import (
    ListTagsForResourceRequest,
    ListTagsForResourceResponse,
)
from async_boto.validation.timestream_write.resume_batch_load_task import (
    ResumeBatchLoadTaskRequest,
    ResumeBatchLoadTaskResponse,
)
from async_boto.validation.timestream_write.tag_resource import (
    TagResourceRequest,
    TagResourceResponse,
)
from async_boto.validation.timestream_write.untag_resource import (
    UntagResourceRequest,
    UntagResourceResponse,
)
from async_boto.validation.timestream_write.update_database import (
    UpdateDatabaseRequest,
    UpdateDatabaseResponse,
)
from async_boto.validation.timestream_write.update_table import (
    UpdateTableRequest,
    UpdateTableResponse,
)
from async_boto.validation.timestream_write.write_records import (
    WriteRecordsRequest,
    WriteRecordsResponse,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AsyncTimestreamWriteClient(BaseClient):
    def __init__(self, aws_session: boto3.Session | AsyncAWSSession):
        super().__init__(aws_session=aws_session, service_name="timestream")
        self._url = (
            f"https://ingest.timestream.{self._aws_session.region_name}.amazonaws.com"
        )

    async def _make_request(
        self, target: str, request: BaseModel, response_cls: type[T], url: str = None
    ) -> T:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
            "X-Amz-Target": target,
        }
        resp = await self._post(
            url=url or self._url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        print(resp.json)
        resp.raise_for_status()
        return response_cls(**resp.json)

    async def describe_endpoints(self):
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
            "X-Amz-Target": "Timestream_20181101.DescribeEndpoints",
            "x-amz-api-version": "2018-11-01",
        }
        resp = await self._post(url=self._url, headers=headers, json={})
        print(resp.json)
        resp.raise_for_status()
        return DescribeEndpointsResponse(**resp.json)

    async def create_batch_load_task(
        self, request: CreateBatchLoadTaskRequest
    ) -> CreateBatchLoadTaskResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.CreateBatchLoadTask",
            request,
            CreateBatchLoadTaskResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def create_database(
        self, request: CreateDatabaseRequest
    ) -> CreateDatabaseResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.CreateDatabase",
            request,
            CreateDatabaseResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def create_table(self, request: CreateTableRequest) -> CreateTableResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.CreateTable",
            request,
            CreateTableResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def delete_database(
        self, request: DeleteDatabaseRequest
    ) -> DeleteDatabaseResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.DeleteDatabase",
            request,
            DeleteDatabaseResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def delete_table(self, request: DeleteTableRequest) -> DeleteTableResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.DeleteTable",
            request,
            DeleteTableResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def describe_batch_load_task(
        self, request: DescribeBatchLoadTaskRequest
    ) -> DescribeBatchLoadTaskResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.DescribeBatchLoadTask",
            request,
            DescribeBatchLoadTaskResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def describe_database(
        self, request: DescribeDatabaseRequest
    ) -> DescribeDatabaseResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.DescribeDatabase",
            request,
            DescribeDatabaseResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def describe_table(
        self, request: DescribeTableRequest
    ) -> DescribeTableResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.DescribeTable",
            request,
            DescribeTableResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def list_batch_load_tasks(
        self, request: ListBatchLoadTasksRequest
    ) -> ListBatchLoadTasksResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.ListBatchLoadTasks",
            request,
            ListBatchLoadTasksResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def list_databases(
        self, request: ListDatabasesRequest
    ) -> ListDatabasesResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.ListDatabases",
            request,
            ListDatabasesResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def list_tables(self, request: ListTablesRequest) -> ListTablesResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.ListTables",
            request,
            ListTablesResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def list_tags_for_resource(
        self, request: ListTagsForResourceRequest
    ) -> ListTagsForResourceResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.ListTagsForResource",
            request,
            ListTagsForResourceResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def resume_batch_load_task(
        self, request: ResumeBatchLoadTaskRequest
    ) -> ResumeBatchLoadTaskResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.ResumeBatchLoadTask",
            request,
            ResumeBatchLoadTaskResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def tag_resource(self, request: TagResourceRequest) -> TagResourceResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.TagResource",
            request,
            TagResourceResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def untag_resource(
        self, request: UntagResourceRequest
    ) -> UntagResourceResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.UntagResource",
            request,
            UntagResourceResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def update_database(
        self, request: UpdateDatabaseRequest
    ) -> UpdateDatabaseResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.UpdateDatabase",
            request,
            UpdateDatabaseResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def update_table(self, request: UpdateTableRequest) -> UpdateTableResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.UpdateTable",
            request,
            UpdateTableResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def write_records(self, request: WriteRecordsRequest) -> WriteRecordsResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.WriteRecords",
            request,
            WriteRecordsResponse,
            url=f"https://{endpoint_to_use.Address}",
        )
