from pydantic import BaseModel, constr


class ListFunctionsByCodeSigningConfigRequest(BaseModel):
    """
    Request model for listing functions by code signing configuration.

    Attributes
    ----------
    CodeSigningConfigArn : str
        The Amazon Resource Name (ARN) of the code signing configuration.
    Marker : str
        Specify the pagination token that's returned by a previous request to retrieve
        the next page of results.
    MaxItems : int
        Maximum number of items to return.
    """

    CodeSigningConfigArn: constr(
        max_length=200,
        pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}((-gov)|(-iso(b?)))?-[a-z]+-\d{1}:\d{12}:code-signing-config:csc-[a-z0-9]{17}",  # noqa: E501
    )
    Marker: str | None
    MaxItems: int | None


class ListFunctionsByCodeSigningConfigResponse(BaseModel):
    """
    Response model for listing functions by code signing configuration.

    Attributes
    ----------
    FunctionArns : list
        The function ARNs.
    NextMarker : str
        The pagination token that's included if more results are available.
    """

    FunctionArns: list[
        constr(
            pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}(-gov)?-[a-z]+-\d{1}:\d{12}:function:[a-zA-Z0-9-_]+(:(\$LATEST|[a-zA-Z0-9-_]+))?"  # noqa: E501
        )
    ]
    NextMarker: str | None
