import logging
from typing import TypeVar

import boto3
from pydantic import BaseModel

from async_boto.core.base_client import BaseClient
from async_boto.core.session import AsyncAWSSession
from async_boto.utils.paginate import paginate
from async_boto.validation.dynamodb.batch_execute_statement import (
    BatchExecuteStatementRequest,
    BatchExecuteStatementResponse,
)
from async_boto.validation.dynamodb.batch_get_item import (
    BatchGetItemRequest,
    BatchGetItemResponse,
)
from async_boto.validation.dynamodb.batch_write_items import (
    BatchWriteItemRequest,
    BatchWriteItemsResponse,
)
from async_boto.validation.dynamodb.create_backup import (
    CreateBackupRequest,
    CreateBackupResponse,
)
from async_boto.validation.dynamodb.create_global_table import (
    CreateGlobalTableRequest,
    CreateGlobalTableResponse,
)
from async_boto.validation.dynamodb.create_table import (
    CreateTableRequest,
    CreateTableResponse,
)
from async_boto.validation.dynamodb.delete_backup import (
    DeleteBackupRequest,
    DeleteBackupResponse,
)
from async_boto.validation.dynamodb.delete_item import (
    DeleteItemRequest,
    DeleteItemResponse,
)
from async_boto.validation.dynamodb.delete_resource_policy import (
    DeleteResourcePolicyRequest,
    DeleteResourcePolicyResponse,
)
from async_boto.validation.dynamodb.delete_table import (
    DeleteTableRequest,
    DeleteTableResponse,
)
from async_boto.validation.dynamodb.describe_backup import (
    DescribeBackupRequest,
    DescribeBackupResponse,
)
from async_boto.validation.dynamodb.describe_continous_backups import (
    DescribeContinuousBackupsRequest,
    DescribeContinuousBackupsResponse,
)
from async_boto.validation.dynamodb.describe_contributor_insights import (
    DescribeContributorInsightsRequest,
    DescribeContributorInsightsResponse,
)
from async_boto.validation.dynamodb.describe_enpoints import DescribeEndpointsResponse
from async_boto.validation.dynamodb.describe_export import (
    DescribeExportRequest,
    DescribeExportResponse,
)
from async_boto.validation.dynamodb.describe_global_table import (
    DescribeGlobalTableRequest,
    DescribeGlobalTableResponse,
)
from async_boto.validation.dynamodb.describe_global_table_settings import (
    DescribeGlobalTableSettingsRequest,
    DescribeGlobalTableSettingsResponse,
)
from async_boto.validation.dynamodb.describe_import import (
    DescribeImportRequest,
    DescribeImportResponse,
)
from async_boto.validation.dynamodb.describe_kinesis_streaming_destination import (
    DescribeKinesisStreamingDestinationRequest,
    DescribeKinesisStreamingDestinationResponse,
)
from async_boto.validation.dynamodb.describe_table import (
    DescribeTableRequest,
    DescribeTableResponse,
)
from async_boto.validation.dynamodb.describe_table_replica_auto_scaling import (
    DescribeTableReplicaAutoScalingRequest,
    DescribeTableReplicaAutoScalingResponse,
)
from async_boto.validation.dynamodb.describe_time_to_live import (
    DescribeTimeToLiveRequest,
    DescribeTimeToLiveResponse,
)
from async_boto.validation.dynamodb.disable_kinesis_streaming_destination import (
    DisableKinesisStreamingDestinationRequest,
    DisableKinesisStreamingDestinationResponse,
)
from async_boto.validation.dynamodb.enable_kinesis_streaming_destination import (
    EnableKinesisStreamingDestinationRequest,
    EnableKinesisStreamingDestinationResponse,
)
from async_boto.validation.dynamodb.execute_statement import (
    ExecuteStatementRequest,
    ExecuteStatementResponse,
)
from async_boto.validation.dynamodb.execute_transaction import (
    ExecuteTransactionRequest,
    ExecuteTransactionResponse,
)
from async_boto.validation.dynamodb.export_table_to_point_in_time import (
    ExportTableToPointInTimeRequest,
    ExportTableToPointInTimeResponse,
)
from async_boto.validation.dynamodb.get_item import GetItemRequest, GetItemResponse
from async_boto.validation.dynamodb.get_resource_policy import (
    GetResourcePolicyRequest,
    GetResourcePolicyResponse,
)
from async_boto.validation.dynamodb.import_table import (
    ImportTableRequest,
    ImportTableResponse,
)
from async_boto.validation.dynamodb.list_backups import (
    ListBackupsRequest,
    ListBackupsResponse,
)
from async_boto.validation.dynamodb.list_contributor_insights import (
    ListContributorInsightsRequest,
    ListContributorInsightsResponse,
)
from async_boto.validation.dynamodb.list_exports import (
    ListExportsRequest,
    ListExportsResponse,
)
from async_boto.validation.dynamodb.list_global_tables import (
    ListGlobalTablesRequest,
    ListGlobalTablesResponse,
)
from async_boto.validation.dynamodb.list_imports import (
    ListImportsRequest,
    ListImportsResponse,
)
from async_boto.validation.dynamodb.list_tables import (
    ListTablesRequest,
    ListTablesResponse,
)
from async_boto.validation.dynamodb.list_tags_of_resource import (
    ListTagsOfResourceRequest,
    ListTagsOfResourceResponse,
)
from async_boto.validation.dynamodb.put_item import PutItemRequest, PutItemResponse
from async_boto.validation.dynamodb.put_resource_policy import (
    PutResourcePolicyRequest,
    PutResourcePolicyResponse,
)
from async_boto.validation.dynamodb.query import QueryRequest, QueryResponse
from async_boto.validation.dynamodb.restore_table_from_backup import (
    RestoreTableFromBackupRequest,
    RestoreTableFromBackupResponse,
)
from async_boto.validation.dynamodb.restore_table_to_point_in_time import (
    RestoreTableToPointInTimeRequest,
    RestoreTableToPointInTimeResponse,
)
from async_boto.validation.dynamodb.scan import ScanRequest, ScanResponse
from async_boto.validation.dynamodb.tag_resource import (
    TagResourceRequest,
    TagResourceResponse,
)
from async_boto.validation.dynamodb.transact_get_items import (
    TransactGetItemsRequest,
    TransactGetItemsResponse,
)
from async_boto.validation.dynamodb.transact_write_items import (
    TransactWriteItemsRequest,
    TransactWriteItemsResponse,
)
from async_boto.validation.dynamodb.untag_resource import (
    UntagResourceRequest,
    UntagResourceResponse,
)
from async_boto.validation.dynamodb.update_continuous_backups import (
    UpdateContinuousBackupsRequest,
    UpdateContinuousBackupsResponse,
)
from async_boto.validation.dynamodb.update_contributor_insights import (
    UpdateContributorInsightsRequest,
    UpdateContributorInsightsResponse,
)
from async_boto.validation.dynamodb.update_global_table import (
    UpdateGlobalTableRequest,
    UpdateGlobalTableResponse,
)
from async_boto.validation.dynamodb.update_global_table_settings import (
    UpdateGlobalTableSettingsRequest,
    UpdateGlobalTableSettingsResponse,
)
from async_boto.validation.dynamodb.update_item import (
    UpdateItemRequest,
    UpdateItemResponse,
)
from async_boto.validation.dynamodb.update_kinesis_streaming_destination import (
    UpdateKinesisStreamingDestinationRequest,
    UpdateKinesisStreamingDestinationResponse,
)
from async_boto.validation.dynamodb.update_table import (
    UpdateTableRequest,
    UpdateTableResponse,
)
from async_boto.validation.dynamodb.update_table_replica_auto_scaling import (
    UpdateTableReplicaAutoScalingRequest,
    UpdateTableReplicaAutoScalingResponse,
)
from async_boto.validation.dynamodb.update_time_to_live import (
    UpdateTimeToLiveRequest,
    UpdateTimeToLiveResponse,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AsyncDynamoDBClient(BaseClient):
    def __init__(
        self, aws_session: boto3.Session | AsyncAWSSession, endpoint_url: str = None
    ):
        super().__init__(aws_session=aws_session, service_name="dynamodb")
        self._url = (
            endpoint_url
            or f"https://dynamodb.{self._aws_session.region_name}.amazonaws.com"
        )

    async def _make_request(
        self, target: str, request: BaseModel, response_cls: type[T]
    ) -> T:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
            "X-Amz-Target": target,
        }
        if request is not None:
            resp = await self._post(
                url=self._url,
                headers=headers,
                json=request.model_dump(exclude_defaults=True, exclude_none=True),
            )
        else:
            resp = await self._post(url=self._url, headers=headers, json={})
        resp.raise_for_status()
        print(resp.json)
        return response_cls(**resp.json)

    async def describe_endpoints(self) -> DescribeEndpointsResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeEndpoints",
            None,
            DescribeEndpointsResponse,
        )

    async def batch_write_items(
        self, request: BatchWriteItemRequest
    ) -> BatchWriteItemsResponse:
        return await self._make_request(
            "DynamoDB_20120810.BatchWriteItem", request, BatchWriteItemsResponse
        )

    async def put_item(self, request: PutItemRequest) -> PutItemResponse:
        return await self._make_request(
            "DynamoDB_20120810.PutItem", request, PutItemResponse
        )

    async def scan(self, request: ScanRequest) -> ScanResponse:
        return await self._make_request("DynamoDB_20120810.Scan", request, ScanResponse)

    async def query(self, request: QueryRequest) -> QueryResponse:
        return await self._make_request(
            "DynamoDB_20120810.Query", request, QueryResponse
        )

    async def describe_table(
        self, request: DescribeTableRequest
    ) -> DescribeTableResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeTable", request, DescribeTableResponse
        )

    async def list_tables(self, request: ListTablesRequest) -> ListTablesResponse:
        return await self._make_request(
            "DynamoDB_20120810.ListTables", request, ListTablesResponse
        )

    async def get_item(self, request: GetItemRequest) -> GetItemResponse:
        return await self._make_request(
            "DynamoDB_20120810.GetItem", request, GetItemResponse
        )

    async def batch_get_item(
        self, request: BatchGetItemRequest
    ) -> BatchGetItemResponse:
        return await self._make_request(
            "DynamoDB_20120810.BatchGetItem", request, BatchGetItemResponse
        )

    async def delete_item(self, request: DeleteItemRequest) -> DeleteItemResponse:
        return await self._make_request(
            "DynamoDB_20120810.DeleteItem", request, DeleteItemResponse
        )

    async def create_backup(self, request: CreateBackupRequest) -> CreateBackupResponse:
        return await self._make_request(
            "DynamoDB_20120810.CreateBackup", request, CreateBackupResponse
        )

    async def batch_execute_statement(
        self, request: BatchExecuteStatementRequest
    ) -> BatchExecuteStatementResponse:
        """
        This operation allows you to perform batch reads or writes on data stored in
        DynamoDB, using PartiQL. Each read statement in a BatchExecuteStatement must
        specify an equality condition on all key attributes.
        This enforces that each SELECT statement in a batch returns at
        most a single item. For more information, see
        [AWS API Docs](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchExecuteStatement.html)

        Parameters
        ----------
        request : BatchExecuteStatementRequest
            The request object containing the parameters for the operation.

        Returns
        -------
        BatchExecuteStatementResponse
            The response object containing the results of the operation.

        Raises
        -------
        async_boto.core.exceptions.ClientError
            if the request fails.

        Examples
        --------
        >>> from tests.async_boto.clients.dynamodb.conftest import dynamodb_client        >>> from async_boto.core.session import AsyncAWSSession
        >>> from async_boto.clients.dynamodb import (
        ...        AsyncDynamoDBClient,
        ...        BatchExecuteStatementRequest,
        ...        BatchExecuteStatementResponse,
        ...        PutItemRequest,
        ...    )
        >>> from async_boto.validation.dynamodb.data_types.batch_statement_request import (
        ...        BatchStatementRequest,
        ...    )
        >>> dynamodb_client = AsyncDynamoDBClient()
        >>> batch_statement_request = BatchStatementRequest(
        ...    Statement=f"SELECT * FROM \"{test_table}\" WHERE hash = 'hash2' and sort='sort2'",
        ...    ConsistentRead=True,
        ... )
        >>> request = BatchExecuteStatementRequest(Statements=[batch_statement_request])
        >>> response = await dynamodb_client.batch_execute_statement(request=request)
        ... 
        >>> assert isinstance(response, BatchExecuteStatementResponse)
        >>> assert response.Responses[0].Item.to_python_dict() == {
        ...     "hash": "hash2",
        ...     "sort": "sort2",
        ... }
        """ # noqa: E501
        return await self._make_request(
            "DynamoDB_20120810.BatchExecuteStatement",
            request,
            BatchExecuteStatementResponse,
        )

    async def create_global_table(
        self, request: CreateGlobalTableRequest
    ) -> CreateGlobalTableResponse:
        return await self._make_request(
            "DynamoDB_20120810.CreateGlobalTable", request, CreateGlobalTableResponse
        )

    async def create_table(self, request: CreateTableRequest) -> CreateTableResponse:
        return await self._make_request(
            "DynamoDB_20120810.CreateTable", request, CreateTableResponse
        )

    async def delete_backup(self, request: DeleteBackupRequest) -> DeleteBackupResponse:
        return await self._make_request(
            "DynamoDB_20120810.DeleteBackup", request, DeleteBackupResponse
        )

    async def delete_resource_policy(
        self, request: DeleteResourcePolicyRequest
    ) -> DeleteResourcePolicyResponse:
        return await self._make_request(
            "DynamoDB_20120810.DeleteResourcePolicy",
            request,
            DeleteResourcePolicyResponse,
        )

    async def delete_table(self, request: DeleteTableRequest) -> DeleteTableResponse:
        return await self._make_request(
            "DynamoDB_20120810.DeleteTable", request, DeleteTableResponse
        )

    async def describe_backup(
        self, request: DescribeBackupRequest
    ) -> DescribeBackupResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeBackup", request, DescribeBackupResponse
        )

    async def describe_continuous_backups(
        self, request: DescribeContinuousBackupsRequest
    ) -> DescribeContinuousBackupsResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeContinuousBackups",
            request,
            DescribeContinuousBackupsResponse,
        )

    async def describe_contributor_insights(
        self, request: DescribeContributorInsightsRequest
    ) -> DescribeContributorInsightsResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeContributorInsights",
            request,
            DescribeContributorInsightsResponse,
        )

    async def describe_export(
        self, request: DescribeExportRequest
    ) -> DescribeExportResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeExport", request, DescribeExportResponse
        )

    async def describe_global_table(
        self, request: DescribeGlobalTableRequest
    ) -> DescribeGlobalTableResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeGlobalTable",
            request,
            DescribeGlobalTableResponse,
        )

    async def describe_global_table_settings(
        self, request: DescribeGlobalTableSettingsRequest
    ) -> DescribeGlobalTableSettingsResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeGlobalTableSettings",
            request,
            DescribeGlobalTableSettingsResponse,
        )

    async def describe_import(
        self, request: DescribeImportRequest
    ) -> DescribeImportResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeImport", request, DescribeImportResponse
        )

    async def describe_kinesis_streaming_destination(
        self, request: DescribeKinesisStreamingDestinationRequest
    ) -> DescribeKinesisStreamingDestinationResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeKinesisStreamingDestination",
            request,
            DescribeKinesisStreamingDestinationResponse,
        )

    async def describe_table_replica_auto_scaling(
        self, request: DescribeTableReplicaAutoScalingRequest
    ) -> DescribeTableReplicaAutoScalingResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeTableReplicaAutoScaling",
            request,
            DescribeTableReplicaAutoScalingResponse,
        )

    async def describe_time_to_live(
        self, request: DescribeTimeToLiveRequest
    ) -> DescribeTimeToLiveResponse:
        return await self._make_request(
            "DynamoDB_20120810.DescribeTimeToLive", request, DescribeTimeToLiveResponse
        )

    async def disable_kinesis_streaming_destination(
        self, request: DisableKinesisStreamingDestinationRequest
    ) -> DisableKinesisStreamingDestinationResponse:
        return await self._make_request(
            "DynamoDB_20120810.DisableKinesisStreamingDestination",
            request,
            DisableKinesisStreamingDestinationResponse,
        )

    async def enable_kinesis_streaming_destination(
        self, request: EnableKinesisStreamingDestinationRequest
    ) -> EnableKinesisStreamingDestinationResponse:
        return await self._make_request(
            "DynamoDB_20120810.EnableKinesisStreamingDestination",
            request,
            EnableKinesisStreamingDestinationResponse,
        )

    async def execute_statement(
        self, request: ExecuteStatementRequest
    ) -> ExecuteStatementResponse:
        return await self._make_request(
            "DynamoDB_20120810.ExecuteStatement", request, ExecuteStatementResponse
        )

    async def execute_transaction(
        self, request: ExecuteTransactionRequest
    ) -> ExecuteTransactionResponse:
        return await self._make_request(
            "DynamoDB_20120810.ExecuteTransaction", request, ExecuteTransactionResponse
        )

    async def export_table_to_point_in_time(
        self, request: ExportTableToPointInTimeRequest
    ) -> ExportTableToPointInTimeResponse:
        return await self._make_request(
            "DynamoDB_20120810.ExportTableToPointInTime",
            request,
            ExportTableToPointInTimeResponse,
        )

    async def get_resource_policy(
        self, request: GetResourcePolicyRequest
    ) -> GetResourcePolicyResponse:
        return await self._make_request(
            "DynamoDB_20120810.GetResourcePolicy", request, GetResourcePolicyResponse
        )

    async def import_table(self, request: ImportTableRequest) -> ImportTableResponse:
        return await self._make_request(
            "DynamoDB_20120810.ImportTable", request, ImportTableResponse
        )

    async def list_backups(self, request: ListBackupsRequest) -> ListBackupsResponse:
        return await self._make_request(
            "DynamoDB_20120810.ListBackups", request, ListBackupsResponse
        )

    async def list_contributor_insights(
        self, request: ListContributorInsightsRequest
    ) -> ListContributorInsightsResponse:
        return await self._make_request(
            "DynamoDB_20120810.ListContributorInsights",
            request,
            ListContributorInsightsResponse,
        )

    async def list_exports(self, request: ListExportsRequest) -> ListExportsResponse:
        return await self._make_request(
            "DynamoDB_20120810.ListExports", request, ListExportsResponse
        )

    async def list_global_tables(
        self, request: ListGlobalTablesRequest
    ) -> ListGlobalTablesResponse:
        return await self._make_request(
            "DynamoDB_20120810.ListGlobalTables", request, ListGlobalTablesResponse
        )

    async def list_imports(self, request: ListImportsRequest) -> ListImportsResponse:
        return await self._make_request(
            "DynamoDB_20120810.ListImports", request, ListImportsResponse
        )

    async def list_tags_of_resource(
        self, request: ListTagsOfResourceRequest
    ) -> ListTagsOfResourceResponse:
        return await self._make_request(
            "DynamoDB_20120810.ListTagsOfResource", request, ListTagsOfResourceResponse
        )

    async def put_resource_policy(
        self, request: PutResourcePolicyRequest
    ) -> PutResourcePolicyResponse:
        return await self._make_request(
            "DynamoDB_20120810.PutResourcePolicy", request, PutResourcePolicyResponse
        )

    async def restore_table_from_backup(
        self, request: RestoreTableFromBackupRequest
    ) -> RestoreTableFromBackupResponse:
        return await self._make_request(
            "DynamoDB_20120810.RestoreTableFromBackup",
            request,
            RestoreTableFromBackupResponse,
        )

    async def restore_table_to_point_in_time(
        self, request: RestoreTableToPointInTimeRequest
    ) -> RestoreTableToPointInTimeResponse:
        return await self._make_request(
            "DynamoDB_20120810.RestoreTableToPointInTime",
            request,
            RestoreTableToPointInTimeResponse,
        )

    async def tag_resource(self, request: TagResourceRequest) -> TagResourceResponse:
        return await self._make_request(
            "DynamoDB_20120810.TagResource", request, TagResourceResponse
        )

    async def transact_get_items(
        self, request: TransactGetItemsRequest
    ) -> TransactGetItemsResponse:
        return await self._make_request(
            "DynamoDB_20120810.TransactGetItems", request, TransactGetItemsResponse
        )

    async def transact_write_items(
        self, request: TransactWriteItemsRequest
    ) -> TransactWriteItemsResponse:
        return await self._make_request(
            "DynamoDB_20120810.TransactWriteItems", request, TransactWriteItemsResponse
        )

    async def untag_resource(
        self, request: UntagResourceRequest
    ) -> UntagResourceResponse:
        return await self._make_request(
            "DynamoDB_20120810.UntagResource", request, UntagResourceResponse
        )

    async def update_continuous_backups(
        self, request: UpdateContinuousBackupsRequest
    ) -> UpdateContinuousBackupsResponse:
        return await self._make_request(
            "DynamoDB_20120810.UpdateContinuousBackups",
            request,
            UpdateContinuousBackupsResponse,
        )

    async def update_contributor_insights(
        self, request: UpdateContributorInsightsRequest
    ) -> UpdateContributorInsightsResponse:
        return await self._make_request(
            "DynamoDB_20120810.UpdateContributorInsights",
            request,
            UpdateContributorInsightsResponse,
        )

    async def update_global_table(
        self, request: UpdateGlobalTableRequest
    ) -> UpdateGlobalTableResponse:
        return await self._make_request(
            "DynamoDB_20120810.UpdateGlobalTable", request, UpdateGlobalTableResponse
        )

    async def update_global_table_settings(
        self, request: UpdateGlobalTableSettingsRequest
    ) -> UpdateGlobalTableSettingsResponse:
        return await self._make_request(
            "DynamoDB_20120810.UpdateGlobalTableSettings",
            request,
            UpdateGlobalTableSettingsResponse,
        )

    async def update_item(self, request: UpdateItemRequest) -> UpdateItemResponse:
        return await self._make_request(
            "DynamoDB_20120810.UpdateItem", request, UpdateItemResponse
        )

    async def update_kinesis_streaming_destination(
        self, request: UpdateKinesisStreamingDestinationRequest
    ) -> UpdateKinesisStreamingDestinationResponse:
        return await self._make_request(
            "DynamoDB_20120810.UpdateKinesisStreamingDestination",
            request,
            UpdateKinesisStreamingDestinationResponse,
        )

    async def update_table(self, request: UpdateTableRequest) -> UpdateTableResponse:
        return await self._make_request(
            "DynamoDB_20120810.UpdateTable", request, UpdateTableResponse
        )

    async def update_table_replica_auto_scaling(
        self, request: UpdateTableReplicaAutoScalingRequest
    ) -> UpdateTableReplicaAutoScalingResponse:
        return await self._make_request(
            "DynamoDB_20120810.UpdateTableReplicaAutoScaling",
            request,
            UpdateTableReplicaAutoScalingResponse,
        )

    async def update_time_to_live(
        self, request: UpdateTimeToLiveRequest
    ) -> UpdateTimeToLiveResponse:
        return await self._make_request(
            "DynamoDB_20120810.UpdateTimeToLive", request, UpdateTimeToLiveResponse
        )

    async def paginate(self, method_name, request: BaseModel):
        paginators = {
            "list_backups": {
                "method": "list_backups",
                "pagination_query_key": "ExclusiveStartBackupArn",
                "pagination_response_key": "LastEvaluatedBackupArn",
            },
            "list_contributor_insights": {
                "method": "list_contributor_insights",
                "pagination_query_key": "NextToken",
                "pagination_response_key": "NextToken",
            },
            "list_exports": {
                "method": "list_exports",
                "pagination_query_key": "NextToken",
                "pagination_response_key": "NextToken",
            },
            "list_global_tables": {
                "method": "list_global_tables",
                "pagination_query_key": "ExclusiveStartGlobalTableName",
                "pagination_response_key": "LastEvaluatedGlobalTableName",
            },
            "list_imports": {
                "method": "list_imports",
                "pagination_query_key": "NextToken",
                "pagination_response_key": "NextToken",
            },
            "list_tables": {
                "method": "list_tables",
                "pagination_query_key": "ExclusiveStartTableName",
                "pagination_response_key": "LastEvaluatedTableName",
            },
            "list_tags_of_resource": {
                "method": "list_tags_of_resource",
                "pagination_query_key": "NextToken",
                "pagination_response_key": "NextToken",
            },
            "query": {
                "method": "query",
                "pagination_query_key": "ExclusiveStartKey",
                "pagination_response_key": "LastEvaluatedKey",
            },
            "scan": {
                "method": "scan",
                "pagination_query_key": "ExclusiveStartKey",
                "pagination_response_key": "LastEvaluatedKey",
            },
        }
        if method_name not in paginators:
            raise ValueError(
                f"Method {method_name} is not paginatable."
                f"Please use any of the following methods: {list(paginators.keys())}"
            )
        paginator = paginate(self, request=request, **paginators[method_name])
        async for page in paginator:
            yield page
