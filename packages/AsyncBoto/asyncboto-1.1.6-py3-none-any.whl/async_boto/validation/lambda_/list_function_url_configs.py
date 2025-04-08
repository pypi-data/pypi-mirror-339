from pydantic import BaseModel, constr

from .data_types.function_url_config import FunctionUrlConfig


class ListFunctionUrlConfigsRequest(BaseModel):
    """
    Request model for listing function URL configs.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    Marker : str
        Specify the pagination token that's returned by a previous request to retrieve
        the next page of results.
    MaxItems : int
        The maximum number of function URLs to return in the response.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Marker: str | None
    MaxItems: int | None


class ListFunctionUrlConfigsResponse(BaseModel):
    """
    Response model for listing function URL configs.

    Attributes
    ----------
    FunctionUrlConfigs : list
        A list of function URL configurations.
    NextMarker : str
        The pagination token that's included if more results are available.
    """

    FunctionUrlConfigs: list[FunctionUrlConfig]
    NextMarker: str | None
