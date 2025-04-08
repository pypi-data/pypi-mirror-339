from pydantic import BaseModel, conint, constr

from .data_types.import_summary import ImportSummary


class ListImportsRequest(BaseModel):
    """
    Request model for the ListImports operation.

    Attributes
    ----------
    NextToken : Optional[str]
        An optional string that, if supplied, must be copied from the output of a
        previous call to ListImports.
    PageSize : Optional[int]
        The number of ImportSummary objects returned in a single page.
    TableArn : Optional[str]
        The Amazon Resource Name (ARN) associated with the table that was imported to.
    """

    NextToken: (
        constr(min_length=112, max_length=1024, pattern=r"([0-9a-f]{16})+") | None
    ) = None  # noqa: E501
    PageSize: conint(ge=1, le=25) | None = None
    TableArn: constr(min_length=1, max_length=1024) | None = None


class ListImportsResponse(BaseModel):
    """
    Response model for the ListImports operation.

    Attributes
    ----------
    ImportSummaryList : Optional[List[ImportSummary]]
        A list of ImportSummary objects.
    NextToken : Optional[str]
        If this value is returned, there are additional results to be displayed.
    """

    ImportSummaryList: list[ImportSummary] | None = None
    NextToken: (
        constr(min_length=112, max_length=1024, pattern=r"([0-9a-f]{16})+") | None
    ) = None  # noqa: E501
