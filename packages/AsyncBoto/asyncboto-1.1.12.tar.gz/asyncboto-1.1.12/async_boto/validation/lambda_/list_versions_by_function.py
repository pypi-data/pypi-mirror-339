from pydantic import BaseModel, conint, constr

from .data_types.function_configuration import FunctionConfiguration


class ListVersionsByFunctionRequest(BaseModel):
    """
    Request model for listing versions of a Lambda function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    Marker : str
        Specify the pagination token that's returned by a previous request to retrieve
        the next page of results.
    MaxItems : int
        The maximum number of versions to return.
    """

    FunctionName: constr(
        min_length=1,
        max_length=170,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_\.]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Marker: str | None
    MaxItems: conint(ge=1, le=10000) | None


class ListVersionsByFunctionResponse(BaseModel):
    """
    Response model for listing versions of a Lambda function.

    Attributes
    ----------
    NextMarker : str
        The pagination token that's included if more results are available.
    Versions : list
        A list of Lambda function versions.
    """

    NextMarker: str | None
    Versions: list[FunctionConfiguration]
