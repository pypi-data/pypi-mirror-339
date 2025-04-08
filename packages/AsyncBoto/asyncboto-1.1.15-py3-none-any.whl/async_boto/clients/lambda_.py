import logging
from typing import TypeVar

import boto3
from pydantic import BaseModel

from async_boto.core.base_client import BaseClient
from async_boto.core.session import AsyncAWSSession
from async_boto.validation.lambda_.add_layer_version_permissions import (
    AddLayerVersionPermissionRequest,
    AddLayerVersionPermissionResponse,
)
from async_boto.validation.lambda_.add_permission import (
    AddPermissionRequest,
    AddPermissionResponse,
)
from async_boto.validation.lambda_.create_alias import (
    CreateAliasRequest,
    CreateAliasResponse,
)
from async_boto.validation.lambda_.create_code_signing_config import (
    CreateCodeSigningConfigRequest,
    CreateCodeSigningConfigResponse,
)
from async_boto.validation.lambda_.create_event_source_mapping import (
    CreateEventSourceMappingRequest,
    CreateEventSourceMappingResponse,
)
from async_boto.validation.lambda_.create_function import (
    CreateFunctionRequest,
    CreateFunctionResponse,
)
from async_boto.validation.lambda_.create_function_url_config import (
    CreateFunctionUrlConfigRequest,
    CreateFunctionUrlConfigResponse,
)
from async_boto.validation.lambda_.delete_alias import (
    DeleteAliasRequest,
    DeleteAliasResponse,
)
from async_boto.validation.lambda_.delete_code_signing_config import (
    DeleteCodeSigningConfigRequest,
    DeleteCodeSigningConfigResponse,
)
from async_boto.validation.lambda_.delete_event_source_mapping import (
    DeleteEventSourceMappingRequest,
    DeleteEventSourceMappingResponse,
)
from async_boto.validation.lambda_.delete_function import (
    DeleteFunctionRequest,
    DeleteFunctionResponse,
)
from async_boto.validation.lambda_.delete_function_code_signing_config import (
    DeleteFunctionCodeSigningConfigRequest,
    DeleteFunctionCodeSigningConfigResponse,
)
from async_boto.validation.lambda_.delete_function_concurrency import (
    DeleteFunctionConcurrencyRequest,
    DeleteFunctionConcurrencyResponse,
)
from async_boto.validation.lambda_.delete_function_event_invoke_config import (
    DeleteFunctionEventInvokeConfigRequest,
    DeleteFunctionEventInvokeConfigResponse,
)
from async_boto.validation.lambda_.delete_function_url_config import (
    DeleteFunctionUrlConfigRequest,
    DeleteFunctionUrlConfigResponse,
)
from async_boto.validation.lambda_.delete_layer_version import (
    DeleteLayerVersionRequest,
    DeleteLayerVersionResponse,
)
from async_boto.validation.lambda_.delete_provisioned_concurrency_config import (
    DeleteProvisionedConcurrencyConfigRequest,
    DeleteProvisionedConcurrencyConfigResponse,
)
from async_boto.validation.lambda_.get_account_settings import (
    GetAccountSettingsRequest,
    GetAccountSettingsResponse,
)
from async_boto.validation.lambda_.get_alias import GetAliasRequest, GetAliasResponse
from async_boto.validation.lambda_.get_code_signing_config import (
    GetCodeSigningConfigRequest,
    GetCodeSigningConfigResponse,
)
from async_boto.validation.lambda_.get_event_source_mapping import (
    GetEventSourceMappingRequest,
    GetEventSourceMappingResponse,
)
from async_boto.validation.lambda_.get_function import (
    GetFunctionRequest,
    GetFunctionResponse,
)
from async_boto.validation.lambda_.get_function_code_signing_config import (
    GetFunctionCodeSigningConfigRequest,
    GetFunctionCodeSigningConfigResponse,
)
from async_boto.validation.lambda_.get_function_concurrency import (
    GetFunctionConcurrencyRequest,
    GetFunctionConcurrencyResponse,
)
from async_boto.validation.lambda_.get_function_configuration import (
    GetFunctionConfigurationRequest,
    GetFunctionConfigurationResponse,
)
from async_boto.validation.lambda_.get_function_event_invoke_config import (
    GetFunctionEventInvokeConfigRequest,
    GetFunctionEventInvokeConfigResponse,
)
from async_boto.validation.lambda_.get_function_recursion_config import (
    GetFunctionRecursionConfigRequest,
    GetFunctionRecursionConfigResponse,
)
from async_boto.validation.lambda_.get_function_url_config import (
    GetFunctionUrlConfigRequest,
    GetFunctionUrlConfigResponse,
)
from async_boto.validation.lambda_.get_layer_version import (
    GetLayerVersionRequest,
    GetLayerVersionResponse,
)
from async_boto.validation.lambda_.get_layer_version_by_arn import (
    GetLayerVersionByArnRequest,
    GetLayerVersionByArnResponse,
)
from async_boto.validation.lambda_.get_layer_version_policy import (
    GetLayerVersionPolicyRequest,
    GetLayerVersionPolicyResponse,
)
from async_boto.validation.lambda_.get_policy import GetPolicyRequest, GetPolicyResponse
from async_boto.validation.lambda_.get_provisioned_concurrency_config import (
    GetProvisionedConcurrencyConfigRequest,
    GetProvisionedConcurrencyConfigResponse,
)
from async_boto.validation.lambda_.get_runtime_management_config import (
    GetRuntimeManagementConfigRequest,
    GetRuntimeManagementConfigResponse,
)
from async_boto.validation.lambda_.invoke import InvokeRequest, InvokeResponse
from async_boto.validation.lambda_.invoke_async import (
    InvokeAsyncRequest,
    InvokeAsyncResponse,
)
from async_boto.validation.lambda_.invoke_with_response_stream import (
    InvokeWithResponseStreamRequest,
    InvokeWithResponseStreamResponse,
)
from async_boto.validation.lambda_.list_aliases import (
    ListAliasesRequest,
    ListAliasesResponse,
)
from async_boto.validation.lambda_.list_code_signing_configs import (
    ListCodeSigningConfigsRequest,
    ListCodeSigningConfigsResponse,
)
from async_boto.validation.lambda_.list_event_source_mappings import (
    ListEventSourceMappingsRequest,
    ListEventSourceMappingsResponse,
)
from async_boto.validation.lambda_.list_function_event_invoke_configs import (
    ListFunctionEventInvokeConfigsRequest,
    ListFunctionEventInvokeConfigsResponse,
)
from async_boto.validation.lambda_.list_function_url_configs import (
    ListFunctionUrlConfigsRequest,
    ListFunctionUrlConfigsResponse,
)
from async_boto.validation.lambda_.list_functions import (
    ListFunctionsRequest,
    ListFunctionsResponse,
)
from async_boto.validation.lambda_.list_functions_by_code_signing_config import (
    ListFunctionsByCodeSigningConfigRequest,
    ListFunctionsByCodeSigningConfigResponse,
)
from async_boto.validation.lambda_.list_layer_versions import (
    ListLayerVersionsRequest,
    ListLayerVersionsResponse,
)
from async_boto.validation.lambda_.list_layers import (
    ListLayersRequest,
    ListLayersResponse,
)
from async_boto.validation.lambda_.list_provisioned_concurrency_configs import (
    ListProvisionedConcurrencyConfigsRequest,
    ListProvisionedConcurrencyConfigsResponse,
)
from async_boto.validation.lambda_.list_tags import (
    ListTagsRequest,
    ListTagsResponse,
)
from async_boto.validation.lambda_.list_versions_by_function import (
    ListVersionsByFunctionRequest,
    ListVersionsByFunctionResponse,
)
from async_boto.validation.lambda_.publish_version import (
    PublishVersionRequest,
    PublishVersionResponse,
)
from async_boto.validation.lambda_.put_function_code_signing_config import (
    PutFunctionCodeSigningConfigRequest,
    PutFunctionCodeSigningConfigResponse,
)
from async_boto.validation.lambda_.put_function_concurrency import (
    PutFunctionConcurrencyRequest,
    PutFunctionConcurrencyResponse,
)
from async_boto.validation.lambda_.put_function_event_invoke_config import (
    PutFunctionEventInvokeConfigRequest,
    PutFunctionEventInvokeConfigResponse,
)
from async_boto.validation.lambda_.put_function_recursion_config import (
    PutFunctionRecursionConfigRequest,
    PutFunctionRecursionConfigResponse,
)
from async_boto.validation.lambda_.put_provisioned_concurrency_config import (
    PutProvisionedConcurrencyConfigRequest,
    PutProvisionedConcurrencyConfigResponse,
)
from async_boto.validation.lambda_.put_runtime_management_config import (
    PutRuntimeManagementConfigRequest,
    PutRuntimeManagementConfigResponse,
)
from async_boto.validation.lambda_.remove_layer_version_permission import (
    RemoveLayerVersionPermissionRequest,
    RemoveLayerVersionPermissionResponse,
)
from async_boto.validation.lambda_.remove_permission import (
    RemovePermissionRequest,
    RemovePermissionResponse,
)
from async_boto.validation.lambda_.tag_resource import (
    TagResourceRequest,
    TagResourceResponse,
)
from async_boto.validation.lambda_.untag_resource import (
    UntagResourceRequest,
    UntagResourceResponse,
)
from async_boto.validation.lambda_.update_alias import (
    UpdateAliasRequest,
    UpdateAliasResponse,
)
from async_boto.validation.lambda_.update_code_signing_config import (
    UpdateCodeSigningConfigRequest,
    UpdateCodeSigningConfigResponse,
)
from async_boto.validation.lambda_.update_event_source_mapping import (
    UpdateEventSourceMappingRequest,
    UpdateEventSourceMappingResponse,
)
from async_boto.validation.lambda_.update_function_code import (
    UpdateFunctionCodeRequest,
    UpdateFunctionCodeResponse,
)
from async_boto.validation.lambda_.update_function_configuration import (
    UpdateFunctionConfigurationRequest,
    UpdateFunctionConfigurationResponse,
)
from async_boto.validation.lambda_.update_function_event_invoke_config import (
    UpdateFunctionEventInvokeConfigRequest,
    UpdateFunctionEventInvokeConfigResponse,
)
from async_boto.validation.lambda_.update_function_url_config import (
    UpdateFunctionUrlConfigRequest,
    UpdateFunctionUrlConfigResponse,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class AsyncLambdaClient(BaseClient):
    def __init__(
        self, aws_session: boto3.Session | AsyncAWSSession, endpoint_url: str = None
    ):
        super().__init__(aws_session=aws_session, service_name="dynamodb")
        self._url = (
            endpoint_url
            or f"https://lambda.{self._aws_session.region_name}.amazonaws.com"
        )

    async def add_layer_version_permission(
        self, request: AddLayerVersionPermissionRequest
    ) -> AddLayerVersionPermissionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            f"{self._url}/2018-10-31/layers/{request.LayerName}/"
            f"versions/{request.VersionNumber}/policy"
        )
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude={"LayerName", "VersionNumber", "RevisionId"},
            ),
            params={"RevisionId": request.RevisionId} if request.RevisionId else {},
        )
        resp.raise_for_status()
        return AddLayerVersionPermissionResponse(**resp.json)

    async def add_permission(
        self, request: AddPermissionRequest
    ) -> AddPermissionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/policy"
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude={"FunctionName", "Qualifier"},
            ),
            params={"Qualifier": request.Qualifier} if request.Qualifier else {},
        )
        resp.raise_for_status()
        return AddPermissionResponse(**resp.json)

    async def create_alias(self, request: CreateAliasRequest) -> CreateAliasResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/aliases"
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude={"FunctionName"},
            ),
        )
        resp.raise_for_status()
        return CreateAliasResponse(**resp.json)

    async def create_code_signing_config(
        self, request: CreateCodeSigningConfigRequest
    ) -> CreateCodeSigningConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + "/2020-04-22/code-signing-configs"
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return CreateCodeSigningConfigResponse(**resp.json)

    async def create_event_source_mapping(
        self, request: CreateEventSourceMappingRequest
    ) -> CreateEventSourceMappingResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + "/2015-03-31/event-source-mappings/"
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return CreateEventSourceMappingResponse(**resp.json)

    async def create_function(
        self, request: CreateFunctionRequest
    ) -> CreateFunctionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + "/2015-03-31/functions"
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return CreateFunctionResponse(**resp.json)

    async def create_function_url_config(
        self, request: CreateFunctionUrlConfigRequest
    ) -> CreateFunctionUrlConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/url-config"
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude={"FunctionName", "Qualifier"},
            ),
            params={"Qualifier": request.Qualifier} if request.Qualifier else {},
        )
        resp.raise_for_status()
        return CreateFunctionUrlConfigResponse(**resp.json)

    async def delete_alias(self, request: DeleteAliasRequest) -> DeleteAliasResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2015-03-31/functions/{request.FunctionName}/aliases/{request.Name}"
        )
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return DeleteAliasResponse(**resp.json)

    async def delete_code_signing_config(
        self, request: DeleteCodeSigningConfigRequest
    ) -> DeleteCodeSigningConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2020-04-22/code-signing-configs/{request.CodeSigningConfigArn}"
        )
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude={"CodeSigningConfigArn"},
            ),
        )
        resp.raise_for_status()
        return DeleteCodeSigningConfigResponse(**resp.json)

    async def delete_event_source_mapping(
        self, request: DeleteEventSourceMappingRequest
    ) -> DeleteEventSourceMappingResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/event-source-mappings/{request.UUID}"
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True, exclude_none=True, exclude={"UUID"}
            ),
        )
        resp.raise_for_status()
        return DeleteEventSourceMappingResponse(**resp.json)

    async def delete_function(
        self, request: DeleteFunctionRequest
    ) -> DeleteFunctionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}"
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True, exclude_none=True, exclude={"FunctionName"}
            ),
            params={"Qualifier": request.Qualifier} if request.Qualifier else {},
        )
        resp.raise_for_status()
        return DeleteFunctionResponse(**resp.json)

    async def delete_function_code_signing_config(
        self, request: DeleteFunctionCodeSigningConfigRequest
    ) -> DeleteFunctionCodeSigningConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2020-06-30/functions/{request.FunctionName}/code-signing-config"
        )
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True, exclude_none=True, exclude={"FunctionName"}
            ),
        )
        resp.raise_for_status()
        return DeleteFunctionCodeSigningConfigResponse(**resp.json)

    async def delete_function_concurrency(
        self, request: DeleteFunctionConcurrencyRequest
    ) -> DeleteFunctionConcurrencyResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2017-10-31/functions/{request.FunctionName}/concurrency"
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True, exclude_none=True, exclude={"FunctionName"}
            ),
        )
        resp.raise_for_status()
        return DeleteFunctionConcurrencyResponse(**resp.json)

    async def delete_function_event_invoke_config(
        self, request: DeleteFunctionEventInvokeConfigRequest
    ) -> DeleteFunctionEventInvokeConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2019-09-25/functions/{request.FunctionName}/event-invoke-config"
        )
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude={"FunctionName", "Qualifier"},
            ),
            params={"Qualifier": request.Qualifier} if request.Qualifier else {},
        )
        resp.raise_for_status()
        return DeleteFunctionEventInvokeConfigResponse(**resp.json)

    async def delete_function_url_config(
        self, request: DeleteFunctionUrlConfigRequest
    ) -> DeleteFunctionUrlConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2021-10-31/functions/{request.FunctionName}/url"
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude={"FunctionName", "Qualifier"},
            ),
            params={"Qualifier": request.Qualifier} if request.Qualifier else {},
        )
        resp.raise_for_status()
        return DeleteFunctionUrlConfigResponse()

    async def delete_layer_version(
        self, request: DeleteLayerVersionRequest
    ) -> DeleteLayerVersionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2018-10-31/layers/{request.LayerName}/versions/{request.VersionNumber}"
        )
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude={"LayerName", "VersionNumber"},
            ),
        )
        resp.raise_for_status()
        return DeleteLayerVersionResponse()

    async def delete_provisioned_concurrency_config(
        self, request: DeleteProvisionedConcurrencyConfigRequest
    ) -> DeleteProvisionedConcurrencyConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2019-09-30/functions/{request.FunctionName}/provisioned-concurrency"
        )
        resp = await self._delete(
            url=url,
            headers=headers,
            json=request.model_dump(
                exclude_defaults=True,
                exclude_none=True,
                exclude={"FunctionName", "Qualifier"},
            ),
            params={"Qualifier": request.Qualifier} if request.Qualifier else {},
        )
        resp.raise_for_status()
        return DeleteProvisionedConcurrencyConfigResponse()

    async def get_account_settings(
        self, request: GetAccountSettingsRequest
    ) -> GetAccountSettingsResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + "/2016-08-19/account-settings/"
        resp = await self._get(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return GetAccountSettingsResponse(**resp.json())

    async def get_alias(self, request: GetAliasRequest) -> GetAliasResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2015-03-31/functions/{request.FunctionName}/aliases/{request.Name}"
        )
        resp = await self._get(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return GetAliasResponse(**resp.json())

    async def get_code_signing_config(
        self, request: GetCodeSigningConfigRequest
    ) -> GetCodeSigningConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2020-04-22/code-signing-configs/{request.CodeSigningConfigArn}"
        )
        resp = await self._get(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return GetCodeSigningConfigResponse(**resp.json())

    async def get_event_source_mapping(
        self, request: GetEventSourceMappingRequest
    ) -> GetEventSourceMappingResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/event-source-mappings/{request.UUID}"
        resp = await self._get(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return GetEventSourceMappingResponse(**resp.json())

    async def get_function(self, request: GetFunctionRequest) -> GetFunctionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}"
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return GetFunctionResponse(**resp.json())

    async def get_function_code_signing_config(
        self, request: GetFunctionCodeSigningConfigRequest
    ) -> GetFunctionCodeSigningConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2020-06-30/functions/{request.FunctionName}/code-signing-config"
        )
        resp = await self._get(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return GetFunctionCodeSigningConfigResponse(**resp.json())

    async def get_function_concurrency(
        self, request: GetFunctionConcurrencyRequest
    ) -> GetFunctionConcurrencyResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2019-09-30/functions/{request.FunctionName}/concurrency"
        resp = await self._get(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return GetFunctionConcurrencyResponse(**resp.json())

    async def get_function_configuration(
        self, request: GetFunctionConfigurationRequest
    ) -> GetFunctionConfigurationResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/configuration"
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return GetFunctionConfigurationResponse(**resp.json())

    async def get_function_event_invoke_config(
        self, request: GetFunctionEventInvokeConfigRequest
    ) -> GetFunctionEventInvokeConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2019-09-25/functions/{request.FunctionName}/event-invoke-config"
        )
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return GetFunctionEventInvokeConfigResponse(**resp.json())

    async def get_function_recursion_config(
        self, request: GetFunctionRecursionConfigRequest
    ) -> GetFunctionRecursionConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url + f"/2024-08-31/functions/{request.FunctionName}/recursion-config"
        )
        resp = await self._get(
            url=url,
            headers=headers,
        )
        resp.raise_for_status()
        return GetFunctionRecursionConfigResponse(**resp.json())

    async def get_function_url_config(
        self, request: GetFunctionUrlConfigRequest
    ) -> GetFunctionUrlConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2021-10-31/functions/{request.FunctionName}/url"
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return GetFunctionUrlConfigResponse(**resp.json())

    async def get_layer_version(
        self, request: GetLayerVersionRequest
    ) -> GetLayerVersionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2018-10-31/layers/{request.LayerName}/versions/{request.VersionNumber}"
        )
        resp = await self._get(
            url=url,
            headers=headers,
        )
        resp.raise_for_status()
        return GetLayerVersionResponse(**resp.json())

    async def get_layer_version_by_arn(
        self, request: GetLayerVersionByArnRequest
    ) -> GetLayerVersionByArnResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2018-10-31/layers?find=LayerVersion&Arn={request.Arn}"
        resp = await self._get(
            url=url,
            headers=headers,
        )
        resp.raise_for_status()
        return GetLayerVersionByArnResponse(**resp.json())

    async def get_layer_version_policy(
        self, request: GetLayerVersionPolicyRequest
    ) -> GetLayerVersionPolicyResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2018-10-31/layers/{request.LayerName}/versions/{request.VersionNumber}/policy"  # noqa: E501
        )
        resp = await self._get(
            url=url,
            headers=headers,
        )
        resp.raise_for_status()
        return GetLayerVersionPolicyResponse(**resp.json())

    async def get_policy(self, request: GetPolicyRequest) -> GetPolicyResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/policy"
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return GetPolicyResponse(**resp.json())

    async def get_provisioned_concurrency_config(
        self, request: GetProvisionedConcurrencyConfigRequest
    ) -> GetProvisionedConcurrencyConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2019-09-30/functions/{request.FunctionName}/provisioned-concurrency"
        )
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return GetProvisionedConcurrencyConfigResponse(**resp.json())

    async def get_runtime_management_config(
        self, request: GetRuntimeManagementConfigRequest
    ) -> GetRuntimeManagementConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2021-07-20/functions/{request.FunctionName}/runtime-management-config"
        )
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return GetRuntimeManagementConfigResponse(**resp.json())

    async def invoke(self, request: InvokeRequest) -> InvokeResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
            "X-Amz-Invocation-Type": request.InvocationType,
            "X-Amz-Log-Type": request.LogType,
        }
        if request.ClientContext:
            headers["X-Amz-Client-Context"] = request.ClientContext

        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/invocations"
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.Payload,
            params=params,
        )
        resp.raise_for_status()
        return InvokeResponse(
            StatusCode=resp.status_code,
            FunctionError=resp.headers.get("X-Amz-Function-Error"),
            LogResult=resp.headers.get("X-Amz-Log-Result"),
            ExecutedVersion=resp.headers.get("X-Amz-Executed-Version"),
            Payload=resp.json() if resp.content else None,
        )

    async def invoke_async(self, request: InvokeAsyncRequest) -> InvokeAsyncResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2014-11-13/functions/{request.FunctionName}/invoke-async/"
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.InvokeArgs,
        )
        resp.raise_for_status()
        return InvokeAsyncResponse(Status=resp.status_code)

    async def invoke_with_response_stream(
        self, request: InvokeWithResponseStreamRequest
    ) -> InvokeWithResponseStreamResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
            "X-Amz-Invocation-Type": request.InvocationType,
            "X-Amz-Log-Type": request.LogType,
        }
        if request.ClientContext:
            headers["X-Amz-Client-Context"] = request.ClientContext

        url = (
            self._url
            + f"/2021-11-15/functions/{request.FunctionName}/response-streaming-invocations"  # noqa: E501
        )
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.Payload,
            params=params,
        )
        resp.raise_for_status()
        return InvokeWithResponseStreamResponse(
            StatusCode=resp.status_code,
            ExecutedVersion=resp.headers.get("X-Amz-Executed-Version"),
            ResponseStreamContentType=resp.headers.get("Content-Type"),
            **resp.json() if resp.content else None,
        )

    async def list_aliases(self, request: ListAliasesRequest) -> ListAliasesResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/aliases"
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListAliasesResponse(**resp.json())

    async def list_code_signing_configs(
        self, request: ListCodeSigningConfigsRequest
    ) -> ListCodeSigningConfigsResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + "/2020-04-22/code-signing-configs/"
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListCodeSigningConfigsResponse(**resp.json())

    async def list_event_source_mappings(
        self, request: ListEventSourceMappingsRequest
    ) -> ListEventSourceMappingsResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + "/2015-03-31/event-source-mappings/"
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListEventSourceMappingsResponse(**resp.json())

    async def list_function_event_invoke_configs(
        self, request: ListFunctionEventInvokeConfigsRequest
    ) -> ListFunctionEventInvokeConfigsResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2019-09-25/functions/{request.FunctionName}/event-invoke-config/list"
        )
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListFunctionEventInvokeConfigsResponse(**resp.json())

    async def list_functions(
        self, request: ListFunctionsRequest
    ) -> ListFunctionsResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + "/2015-03-31/functions/"
        resp = await self._get(
            url=url,
            headers=headers,
            json={},
            params=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        print(resp.json)
        resp.raise_for_status()
        return ListFunctionsResponse(**resp.json)

    async def list_functions_by_code_signing_config(
        self, request: ListFunctionsByCodeSigningConfigRequest
    ) -> ListFunctionsByCodeSigningConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2020-04-22/code-signing-configs/{request.CodeSigningConfigArn}/functions"  # noqa: E501
        )
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListFunctionsByCodeSigningConfigResponse(**resp.json())

    async def list_function_url_configs(
        self, request: ListFunctionUrlConfigsRequest
    ) -> ListFunctionUrlConfigsResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2021-10-31/functions/{request.FunctionName}/urls"
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListFunctionUrlConfigsResponse(**resp.json())

    async def list_layers(self, request: ListLayersRequest) -> ListLayersResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + "/2018-10-31/layers"
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListLayersResponse(**resp.json())

    async def list_layer_versions(
        self, request: ListLayerVersionsRequest
    ) -> ListLayerVersionsResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2018-10-31/layers/{request.LayerName}/versions"
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListLayerVersionsResponse(**resp.json())

    async def list_provisioned_concurrency_configs(
        self, request: ListProvisionedConcurrencyConfigsRequest
    ) -> ListProvisionedConcurrencyConfigsResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2019-09-30/functions/{request.FunctionName}/provisioned-concurrency"
        )
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListProvisionedConcurrencyConfigsResponse(**resp.json())

    async def list_tags(self, request: ListTagsRequest) -> ListTagsResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2017-03-31/tags/{request.ARN}"
        resp = await self._get(
            url=url,
            headers=headers,
        )
        resp.raise_for_status()
        return ListTagsResponse(**resp.json())

    async def list_versions_by_function(
        self, request: ListVersionsByFunctionRequest
    ) -> ListVersionsByFunctionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/versions"
        params = request.model_dump(exclude_defaults=True, exclude_none=True)
        resp = await self._get(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return ListVersionsByFunctionResponse(**resp.json())

    async def publish_version(
        self, request: PublishVersionRequest
    ) -> PublishVersionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/versions"
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return PublishVersionResponse(**resp.json())

    async def put_function_code_signing_config(
        self, request: PutFunctionCodeSigningConfigRequest
    ) -> PutFunctionCodeSigningConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2020-06-30/functions/{request.FunctionName}/code-signing-config"
        )
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return PutFunctionCodeSigningConfigResponse(**resp.json())

    async def put_function_concurrency(
        self, request: PutFunctionConcurrencyRequest
    ) -> PutFunctionConcurrencyResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2017-10-31/functions/{request.FunctionName}/concurrency"
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return PutFunctionConcurrencyResponse(**resp.json())

    async def put_function_event_invoke_config(
        self, request: PutFunctionEventInvokeConfigRequest
    ) -> PutFunctionEventInvokeConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2019-09-25/functions/{request.FunctionName}/event-invoke-config"
        )
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
            params=params,
        )
        resp.raise_for_status()
        return PutFunctionEventInvokeConfigResponse(**resp.json())

    async def put_function_recursion_config(
        self, request: PutFunctionRecursionConfigRequest
    ) -> PutFunctionRecursionConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url + f"/2024-08-31/functions/{request.FunctionName}/recursion-config"
        )
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return PutFunctionRecursionConfigResponse(**resp.json())

    async def put_provisioned_concurrency_config(
        self, request: PutProvisionedConcurrencyConfigRequest
    ) -> PutProvisionedConcurrencyConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2019-09-30/functions/{request.FunctionName}/provisioned-concurrency"
        )
        params = {"Qualifier": request.Qualifier}
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
            params=params,
        )
        resp.raise_for_status()
        return PutProvisionedConcurrencyConfigResponse(**resp.json())

    async def put_runtime_management_config(
        self, request: PutRuntimeManagementConfigRequest
    ) -> PutRuntimeManagementConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2021-07-20/functions/{request.FunctionName}/runtime-management-config"
        )
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
            params=params,
        )
        resp.raise_for_status()
        return PutRuntimeManagementConfigResponse(**resp.json())

    async def remove_layer_version_permission(
        self, request: RemoveLayerVersionPermissionRequest
    ) -> RemoveLayerVersionPermissionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2018-10-31/layers/{request.LayerName}/versions/{request.VersionNumber}/policy/{request.StatementId}"  # noqa: E501
        )
        params = {"RevisionId": request.RevisionId} if request.RevisionId else {}
        resp = await self._delete(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return RemoveLayerVersionPermissionResponse()

    async def remove_permission(
        self, request: RemovePermissionRequest
    ) -> RemovePermissionResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2015-03-31/functions/{request.FunctionName}/policy/{request.StatementId}"  # noqa: E501
        )
        params = {}
        if request.Qualifier:
            params["Qualifier"] = request.Qualifier
        if request.RevisionId:
            params["RevisionId"] = request.RevisionId
        resp = await self._delete(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return RemovePermissionResponse()

    async def tag_resource(self, request: TagResourceRequest) -> TagResourceResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2017-03-31/tags/{request.ARN}"
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return TagResourceResponse()

    async def untag_resource(
        self, request: UntagResourceRequest
    ) -> UntagResourceResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2017-03-31/tags/{request.ARN}"
        params = {"tagKeys": request.TagKeys}
        resp = await self._delete(
            url=url,
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        return UntagResourceResponse()

    async def update_alias(self, request: UpdateAliasRequest) -> UpdateAliasResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2015-03-31/functions/{request.FunctionName}/aliases/{request.Name}"
        )
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return UpdateAliasResponse(**resp.json())

    async def update_code_signing_config(
        self, request: UpdateCodeSigningConfigRequest
    ) -> UpdateCodeSigningConfigResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = (
            self._url
            + f"/2020-04-22/code-signing-configs/{request.CodeSigningConfigArn}"
        )
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return UpdateCodeSigningConfigResponse(**resp.json())

    async def update_event_source_mapping(
        self, request: UpdateEventSourceMappingRequest
    ) -> UpdateEventSourceMappingResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/event-source-mappings/{request.UUID}"
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return UpdateEventSourceMappingResponse(**resp.json())

    async def update_function_code(
        self, request: UpdateFunctionCodeRequest
    ) -> UpdateFunctionCodeResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/code"
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return UpdateFunctionCodeResponse(**resp.json())

    async def update_function_configuration(
        self, request: UpdateFunctionConfigurationRequest
    ) -> UpdateFunctionConfigurationResponse:
        headers = {
            "Content-Type": "application/x-amz-json-1.0",
        }
        url = self._url + f"/2015-03-31/functions/{request.FunctionName}/configuration"
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
        )
        resp.raise_for_status()
        return UpdateFunctionConfigurationResponse(**resp.json())

    async def update_function_event_invoke_config(
        self, request: UpdateFunctionEventInvokeConfigRequest
    ) -> UpdateFunctionEventInvokeConfigResponse:
        """
        Updates the configuration for asynchronous invocation for a function, version,
        or alias.
        """
        headers = {
            "Content-Type": "application/json",
        }
        url = (
            self._url
            + f"/2019-09-25/functions/{request.FunctionName}/event-invoke-config"
        )
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._post(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
            params=params,
        )
        resp.raise_for_status()
        return UpdateFunctionEventInvokeConfigResponse(**resp.json())

    async def update_function_url_config(
        self, request: UpdateFunctionUrlConfigRequest
    ) -> UpdateFunctionUrlConfigResponse:
        """
        Updates the configuration for a Lambda function URL.

        Parameters
        ----------
        request : UpdateFunctionUrlConfigRequest
            The request model containing the parameters for updating the function URL
            configuration.

        Returns
        -------
        UpdateFunctionUrlConfigResponse
            The response model containing the updated function URL configuration.
        """
        headers = {
            "Content-Type": "application/json",
        }
        url = self._url + f"/2021-10-31/functions/{request.FunctionName}/url"
        params = {"Qualifier": request.Qualifier} if request.Qualifier else {}
        resp = await self._put(
            url=url,
            headers=headers,
            json=request.model_dump(exclude_defaults=True, exclude_none=True),
            params=params,
        )
        resp.raise_for_status()
        return UpdateFunctionUrlConfigResponse(**resp.json())
