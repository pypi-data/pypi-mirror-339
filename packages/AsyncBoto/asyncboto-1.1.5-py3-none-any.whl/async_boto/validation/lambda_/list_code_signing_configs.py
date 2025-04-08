from pydantic import BaseModel

from .data_types.code_signing_config import CodeSigningConfig


class ListCodeSigningConfigsRequest(BaseModel):
    """
    Request model for listing code signing configurations.

    Attributes
    ----------
    Marker : str
        Specify the pagination token that's returned by a previous request to
        retrieve the next page of results.
    MaxItems : int
        Maximum number of items to return.
    """

    Marker: str | None
    MaxItems: int | None


class ListCodeSigningConfigsResponse(BaseModel):
    """
    Response model for listing code signing configurations.

    Attributes
    ----------
    CodeSigningConfigs : list
        The code signing configurations.
    NextMarker : str
        The pagination token that's included if more results are available.
    """

    CodeSigningConfigs: list[CodeSigningConfig]
    NextMarker: str | None
