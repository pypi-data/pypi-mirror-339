import logging
import random
from typing import TypeVar

import boto3
from pydantic import BaseModel

from async_boto.core.base_client import BaseClient
from async_boto.core.session import AsyncAWSSession
from async_boto.validation.timestream_query.cancel_query import (
    CancelQueryRequest,
    CancelQueryResponse,
)
from async_boto.validation.timestream_query.create_scheduled_query import (
    CreateScheduledQueryRequest,
    CreateScheduledQueryResponse,
)
from async_boto.validation.timestream_query.delete_scheduled_query import (
    DeleteScheduledQueryRequest,
    DeleteScheduledQueryResponse,
)
from async_boto.validation.timestream_query.describe_account_settings import (
    DescribeAccountSettingsRequest,
    DescribeAccountSettingsResponse,
)
from async_boto.validation.timestream_query.describe_endpoints import (
    DescribeEndpointsResponse,
)
from async_boto.validation.timestream_query.describe_scheduled_query import (
    DescribeScheduledQueryRequest,
    DescribeScheduledQueryResponse,
)
from async_boto.validation.timestream_query.execute_scheduled_query import (
    ExecuteScheduledQueryRequest,
    ExecuteScheduledQueryResponse,
)
from async_boto.validation.timestream_query.list_scheduled_queries import (
    ListScheduledQueriesRequest,
    ListScheduledQueriesResponse,
)
from async_boto.validation.timestream_query.list_tags_for_resource import (
    ListTagsForResourceRequest,
    ListTagsForResourceResponse,
)
from async_boto.validation.timestream_query.prepare_query import (
    PrepareQueryRequest,
    PrepareQueryResponse,
)
from async_boto.validation.timestream_query.query import QueryRequest, QueryResponse
from async_boto.validation.timestream_query.tag_resource import (
    TagResourceRequest,
    TagResourceResponse,
)
from async_boto.validation.timestream_query.untag_resource import (
    UntagResourceRequest,
    UntagResourceResponse,
)
from async_boto.validation.timestream_query.update_account_settings import (
    UpdateAccountSettingsRequest,
    UpdateAccountSettingsResponse,
)
from async_boto.validation.timestream_query.update_scheduled_query import (
    UpdateScheduledQueryRequest,
    UpdateScheduledQueryResponse,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AsyncTimestreamQueryClient(BaseClient):
    def __init__(self, aws_session: boto3.Session | AsyncAWSSession):
        super().__init__(aws_session=aws_session, service_name="timestream")
        self._url = (
            f"https://query.timestream.{self._aws_session.region_name}.amazonaws.com"
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

    async def cancel_query(self, request: CancelQueryRequest) -> CancelQueryResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.CancelQuery",
            request,
            CancelQueryResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def create_scheduled_query(
        self, request: CreateScheduledQueryRequest
    ) -> CreateScheduledQueryResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.CreateScheduledQuery",
            request,
            CreateScheduledQueryResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def delete_scheduled_query(
        self, request: DeleteScheduledQueryRequest
    ) -> DeleteScheduledQueryResponse:
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.DeleteScheduledQuery",
            request,
            DeleteScheduledQueryResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def describe_account_settings(
        self, request: DescribeAccountSettingsRequest
    ) -> DescribeAccountSettingsResponse:
        """
        Describe the settings for your Timestream account.

        This method retrieves account-specific settings, including the query pricing
        model and the maximum Timestream Compute Units (TCUs) configured for query
        workloads.

        Notes
        -----
        - You are charged only for the duration of compute units used for your
        workloads.

        Parameters
        ----------
        request : DescribeAccountSettingsRequest
            The request object for describing account settings.

        Returns
        -------
        DescribeAccountSettingsResponse
            A response containing the account settings, including:
            - QueryPricingModel: The pricing model for queries
            - MaxQueryTCUs: Maximum TCUs configured for query workloads

        Raises
        ------
        Exception
            If there is an error retrieving the account settings.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.DescribeAccountSettings",
            request,
            DescribeAccountSettingsResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def describe_scheduled_query(
        self, request: DescribeScheduledQueryRequest
    ) -> DescribeScheduledQueryResponse:
        """
        Provides detailed information about a scheduled query.

        Parameters
        ----------
        request : DescribeScheduledQueryRequest
            The request object containing details for the scheduled query to describe.

        Returns
        -------
        DescribeScheduledQueryResponse
            A response object with detailed information about the specified scheduled
            query.

        Raises
        ------
        Exception
            If there is an error retrieving the scheduled query information.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.DescribeScheduledQuery",
            request,
            DescribeScheduledQueryResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def execute_scheduled_query(
        self, request: ExecuteScheduledQueryRequest
    ) -> ExecuteScheduledQueryResponse:
        """
        Manually run a scheduled query.

        This method allows manual execution of a scheduled query. When QueryInsights
        is enabled, the method also returns insights and metrics related to the
        executed query as part of an Amazon SNS notification.

        Notes
        -----
        - QueryInsights can help with performance tuning of your query.
        - For detailed information about QueryInsights, refer to the Amazon
          Timestream documentation on optimizing queries.

        Parameters
        ----------
        request : ExecuteScheduledQueryRequest
            The request object containing details for executing the scheduled query.

        Returns
        -------
        ExecuteScheduledQueryResponse
            A response object with the results of the executed scheduled query,
            and potentially including query insights if enabled.

        Raises
        ------
        Exception
            If there is an error executing the scheduled query.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.ExecuteScheduledQuery",
            request,
            ExecuteScheduledQueryResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def list_scheduled_queries(
        self, request: ListScheduledQueriesRequest
    ) -> ListScheduledQueriesResponse:
        """
        Retrieve a list of all scheduled queries in the current Amazon account and
        Region.

        Notes
        -----
        - This method is eventually consistent, meaning the returned list may not
          immediately reflect all recent changes to scheduled queries.

        Parameters
        ----------
        request : ListScheduledQueriesRequest
            The request object for listing scheduled queries.

        Returns
        -------
        ListScheduledQueriesResponse
            A response object containing the list of scheduled queries.

        Raises
        ------
        Exception
            If there is an error retrieving the list of scheduled queries.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.ListScheduledQueries",
            request,
            ListScheduledQueriesResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def list_tags_for_resource(
        self, request: ListTagsForResourceRequest
    ) -> ListTagsForResourceResponse:
        """
        List all tags associated with a Timestream query resource.

        Parameters
        ----------
        request : ListTagsForResourceRequest
            The request object containing the resource for which to list tags.

        Returns
        -------
        ListTagsForResourceResponse
            A response object containing the list of tags for the specified resource.

        Raises
        ------
        Exception
            If there is an error retrieving the tags for the resource.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.ListTagsForResource",
            request,
            ListTagsForResourceResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def prepare_query(self, request: PrepareQueryRequest) -> PrepareQueryResponse:
        """
        Submit a query with parameters to be stored by Timestream for later running.

        Notes
        -----
        - This is a synchronous operation.
        - Timestream currently only supports using this operation with
          `ValidateOnly` set to `true`.

        Parameters
        ----------
        request : PrepareQueryRequest
            The request object containing the query to be prepared.
            The `ValidateOnly` parameter should be set to `true`.

        Returns
        -------
        PrepareQueryResponse
            A response object containing the result of the query preparation.

        Raises
        ------
        Exception
            If there is an error preparing the query.

        Warnings
        --------
        Ensure that the `ValidateOnly` parameter is set to `true` as
        Timestream currently only supports validation mode.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.PrepareQuery",
            request,
            PrepareQueryResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def query(self, request: QueryRequest) -> QueryResponse:
        """
        Run a synchronous query against Amazon Timestream data.

        Notes
        -----
        - Supports QueryInsights for performance tuning when enabled.
        - Strict usage constraints and limitations apply:
            * Maximum 1 query per second (QPS) with QueryInsights enabled
            * Query timeout is 60 seconds
            * Idempotency window of 5 minutes for client tokens
            * Maximum row size (including metadata) is 1 MB

        Warnings
        --------
        Query will fail under the following conditions:
        - Submitting a query with the same client token outside the 5-minute idempotency
          window
        - Changing parameters while using the same client token within the idempotency
          window
        - Row size (including query metadata) exceeding 1 MB
        - IAM principal mismatch between query initiator and result reader
        - Different query strings for query initiator and result reader

        Parameters
        ----------
        request : QueryRequest
            The request object containing the query to be executed.

        Returns
        -------
        QueryResponse
            A response object containing the query results and potentially
            QueryInsights if enabled.

        Raises
        ------
        Exception
            If there is an error executing the query or if any of the
            specified conditions are violated.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.Query",
            request,
            QueryResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def tag_resource(self, request: TagResourceRequest) -> TagResourceResponse:
        """
        Associate a set of tags with a Timestream resource.

        Notes
        -----
        - Tagged resources can be activated for cost allocation tracking.
        - Tags will appear on the Billing and Cost Management console.

        Parameters
        ----------
        request : TagResourceRequest
            The request object containing the resource and tags to be associated.

        Returns
        -------
        TagResourceResponse
            A response object indicating the result of the tagging operation.

        Raises
        ------
        Exception
            If there is an error associating tags with the resource.
        """
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
        """
        Remove the association of tags from a Timestream query resource.

        Parameters
        ----------
        request : UntagResourceRequest
            The request object containing the resource and tags to be removed.

        Returns
        -------
        UntagResourceResponse
            A response object indicating the result of the untagging operation.

        Raises
        ------
        Exception
            If there is an error removing tags from the resource.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.UntagResource",
            request,
            UntagResourceResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def update_account_settings(
        self, request: UpdateAccountSettingsRequest
    ) -> UpdateAccountSettingsResponse:
        """
        Update account settings for Timestream query pricing and compute units.

        Notes
        -----
        - Transitions the account to use Timestream Compute Units (TCUs) for
          query pricing.
        - Modifies the maximum query compute units configuration.
        - Reducing MaxQueryTCU may take up to 24 hours to become effective.
        - Once transitioned to TCUs, you cannot revert to bytes scanned pricing.

        Parameters
        ----------
        request : UpdateAccountSettingsRequest
            The request object containing the updated account settings.

        Returns
        -------
        UpdateAccountSettingsResponse
            A response object indicating the result of the account settings update.

        Raises
        ------
        Exception
            If there is an error updating the account settings.

        Warnings
        --------
        Changes to MaxQueryTCU may have a delayed implementation of up to 24 hours.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.UpdateAccountSettings",
            request,
            UpdateAccountSettingsResponse,
            url=f"https://{endpoint_to_use.Address}",
        )

    async def update_scheduled_query(
        self, request: UpdateScheduledQueryRequest
    ) -> UpdateScheduledQueryResponse:
        """
        Update a scheduled query.

        Parameters
        ----------
        request : UpdateScheduledQueryRequest
            The request object containing the details for updating the scheduled query.

        Returns
        -------
        UpdateScheduledQueryResponse
            A response object indicating the result of the scheduled query update.

        Raises
        ------
        Exception
            If there is an error updating the scheduled query.
        """
        endpoint = await self.describe_endpoints()
        endpoint_to_use = random.choice(endpoint.Endpoints)
        return await self._make_request(
            "Timestream_20181101.UpdateScheduledQuery",
            request,
            UpdateScheduledQueryResponse,
            url=f"https://{endpoint_to_use.Address}",
        )
