from collections.abc import AsyncGenerator
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


async def paginate(
    client: Any,
    method: str,
    request: BaseModel,
    pagination_response_key: str = "LastEvaluatedKey",
    pagination_query_key: str = None,
) -> AsyncGenerator[T, None]:
    """
    Generic paginator function for DynamoDB client methods.

    Parameters
    ----------
    client : Any
        The DynamoDB client instance.
    method : str
        The name of the client method to call.
    request : BaseModel
        The request model instance.
    pagination_response_key : str, optional
        The key in the response that indicates the pagination token,
        by default "LastEvaluatedKey".
    pagination_query_key : str, optional
        The key in the request that indicates the pagination token, by default None.
        If not given, it will be the same as pagination_response_key.

    Yields
    ------
    T
        The response model instance for each page.
    """
    pagination_query_key = pagination_query_key or pagination_response_key

    while True:
        response = await getattr(client, method)(request)
        response_data = response.model_dump()
        yield response

        if (
            pagination_response_key in response_data
            and response_data[pagination_response_key]
        ):
            setattr(
                request, pagination_query_key, response_data[pagination_response_key]
            )
        else:
            break
