from pydantic import BaseModel, conint, constr

from .data_types.contributor_insights_summary import ContributorInsightsSummary


class ListContributorInsightsRequest(BaseModel):
    """
    Request model for the ListContributorInsights operation.

    Attributes
    ----------
    MaxResults : Optional[int]
        Maximum number of results to return per page.
    NextToken : Optional[str]
        A token for the desired page, if there is one.
    TableName : Optional[str]
        The name of the table. You can also provide the Amazon Resource Name (ARN)
        of the table in this parameter.
    """

    MaxResults: conint(le=100) | None = None
    NextToken: str | None = None
    TableName: constr(min_length=1, max_length=1024) | None = None


class ListContributorInsightsResponse(BaseModel):
    """
    Response model for the ListContributorInsights operation.

    Attributes
    ----------
    ContributorInsightsSummaries : Optional[List[ContributorInsightsSummary]]
        A list of ContributorInsightsSummary.
    NextToken : Optional[str]
        A token to go to the next page if there is one.
    """

    ContributorInsightsSummaries: list[ContributorInsightsSummary] | None = None
    NextToken: str | None = None
