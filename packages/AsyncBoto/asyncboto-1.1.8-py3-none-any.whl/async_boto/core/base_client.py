import json as json_
import logging
import traceback
from typing import Any, Literal

import aiohttp
import boto3
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from async_boto.core.session import AsyncAWSSession
from async_boto.utils.generate_param_tuple import generate_param_tuple
from async_boto.utils.json_dumps import json_dump

from .aws_sig_v4_headers import aws_sig_v4_headers
from .response import AsyncRequestResponse

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(
        self,
        aws_session: boto3.Session | AsyncAWSSession,
        service_name: str = "execute-api",
    ) -> None:
        self._aws_session = aws_session
        self._service_name = service_name

    async def _get(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: bytes | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> AsyncRequestResponse:
        return await self._async_request(
            method="GET",
            url=url,
            json=json,
            data=data,
            params=params,
            headers=headers,
        )

    async def _post(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: bytes | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> AsyncRequestResponse:
        return await self._async_request(
            method="POST",
            url=url,
            json=json,
            data=data,
            params=params,
            headers=headers,
        )

    async def _put(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: bytes | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> AsyncRequestResponse:
        return await self._async_request(
            method="PUT",
            url=url,
            json=json,
            data=data,
            params=params,
            headers=headers,
        )

    async def _delete(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: bytes | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> AsyncRequestResponse:
        return await self._async_request(
            method="DELETE",
            url=url,
            json=json,
            data=data,
            params=params,
            headers=headers,
        )

    async def _head(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: bytes | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> AsyncRequestResponse:
        return await self._async_request(
            method="HEAD",
            url=url,
            json=json,
            data=data,
            params=params,
            headers=headers,
        )

    async def _options(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: bytes | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> AsyncRequestResponse:
        return await self._async_request(
            method="OPTIONS",
            url=url,
            json=json,
            data=data,
            params=params,
            headers=headers,
        )

    async def _patch(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: bytes | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> AsyncRequestResponse:
        return await self._async_request(
            method="PATCH",
            url=url,
            json=json,
            data=data,
            params=params,
            headers=headers,
        )

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=10, max=60),
        retry=retry_if_exception_type(aiohttp.client.ClientOSError),
        reraise=True,
    )
    async def _async_request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"],
        url: str,
        json: dict[str, Any] | None = None,
        data: bytes | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> AsyncRequestResponse:
        session = aiohttp.ClientSession()

        if params:
            params = generate_param_tuple(params=params)

        if json is not None:
            data = json_.dumps(
                {key: value for key, value in json.items() if value is not None},
                default=json_dump,
            )
            if not headers.get("Content-Type") or not headers.get("content-type"):
                headers["Content-Type"] = "application/json"

        signed_headers = aws_sig_v4_headers(
            session=self._aws_session,
            headers=headers,
            service=self._service_name,
            url=url,
            query=params,
            payload=data,
            method=method,
        )
        signed_headers = {
            key: value for key, value in signed_headers.items() if value is not None
        }
        try:
            async with session.request(
                method=method, params=params, data=data, url=url, headers=signed_headers
            ) as response:
                print(f"{method=} {params=} {data=} {url=} {headers=}")
                try:
                    resp_json = await response.json(content_type=None)
                except json_.decoder.JSONDecodeError:
                    resp_json = None

                resp_text = await response.text()
                resp = AsyncRequestResponse(
                    status_code=response.status,
                    text=resp_text,
                    json=resp_json,
                    url=response.url,
                    headers=response.headers,
                )
                return resp
        except:  # noqa: E722
            logger.error(traceback.format_exc())
        finally:
            await session.close()
