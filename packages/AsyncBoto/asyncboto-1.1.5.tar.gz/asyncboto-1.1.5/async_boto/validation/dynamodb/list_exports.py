from pydantic import BaseModel, conint, constr

from .data_types.export_summary import ExportSummary


class ListExportsRequest(BaseModel):
    """
    Request model for the ListExports operation.

    Attributes
    ----------
    MaxResults : Optional[int]
        Maximum number of results to return per page.
    NextToken : Optional[str]
        An optional string that, if supplied, must be copied from the output of a
        previous call to ListExports.
    TableArn : Optional[str]
        The Amazon Resource Name (ARN) associated with the exported table.
    """

    MaxResults: conint(ge=1, le=25) | None = None
    NextToken: str | None = None
    TableArn: constr(min_length=1, max_length=1024) | None = None


class ListExportsResponse(BaseModel):
    """
    Response model for the ListExports operation.

    Attributes
    ----------
    ExportSummaries : Optional[List[ExportSummary]]
        A list of ExportSummary objects.
    NextToken : Optional[str]
        If this value is returned, there are additional results to be displayed.
    """

    ExportSummaries: list[ExportSummary] | None = None
    NextToken: str | None = None
