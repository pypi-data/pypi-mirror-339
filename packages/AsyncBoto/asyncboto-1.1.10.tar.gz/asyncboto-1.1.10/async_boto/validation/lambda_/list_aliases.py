from pydantic import BaseModel, constr

from .data_types.alias_configuration import AliasConfiguration


class ListAliasesRequest(BaseModel):
    """
    Request model for listing aliases of a Lambda function.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    FunctionVersion : str
        Specify a function version to only list aliases that invoke that version.
    Marker : str
        Specify the pagination token that's returned by a previous request to retrieve
        the next page of results.
    MaxItems : int
        Limit the number of aliases returned.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    FunctionVersion: (
        constr(min_length=1, max_length=1024, pattern=r"(\$LATEST|[0-9]+)") | None
    )
    Marker: str | None
    MaxItems: int | None


class ListAliasesResponse(BaseModel):
    """
    Response model for listing aliases of a Lambda function.

    Attributes
    ----------
    Aliases : list
        A list of aliases.
    NextMarker : str
        The pagination token that's included if more results are available.
    """

    Aliases: list[AliasConfiguration]
    NextMarker: str | None
