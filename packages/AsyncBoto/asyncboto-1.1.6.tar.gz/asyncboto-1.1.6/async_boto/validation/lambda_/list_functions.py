from typing import Literal

from pydantic import BaseModel, conint, constr

from .data_types.function_configuration import FunctionConfiguration


class ListFunctionsRequest(BaseModel):
    r"""
    Request model for the ListFunctions operation.

    Returns a list of Lambda functions, with the version-specific configuration of each.
    Lambda returns up to 50 functions per call.

    Attributes
    ----------
    FunctionVersion : Optional[Literal["ALL"]]
        Set to ALL to include entries for all published versions of each function.
    Marker : Optional[str]
        Specify the pagination token that's returned by a previous request to retrieve
        the next page of results.
    MasterRegion : Optional[constr(regex=r'ALL|[a-z]{2}(-gov)?-[a-z]+-\d{1}')]
        For Lambda@Edge functions, the AWS Region of the master function.
    MaxItems : Optional[conint(ge=1, le=10000)]
        The maximum number of functions to return in the response.
    """

    FunctionVersion: Literal["ALL"] | None = None
    Marker: str | None = None
    MasterRegion: constr(pattern=r"ALL|[a-z]{2}(-gov)?-[a-z]+-\d{1}") | None = None
    MaxItems: conint(ge=1, le=10000) | None = None


class ListFunctionsResponse(BaseModel):
    """
    Response model for the ListFunctions operation.

    Attributes
    ----------
    Functions : List[FunctionConfiguration]
        A list of Lambda functions.
    NextMarker : Optional[str]
        The pagination token that's included if more results are available.
    """

    Functions: list[FunctionConfiguration] = []
    NextMarker: str | None = None
