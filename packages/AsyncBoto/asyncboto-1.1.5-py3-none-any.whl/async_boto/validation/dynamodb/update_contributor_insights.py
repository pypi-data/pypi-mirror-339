from typing import Literal

from pydantic import BaseModel, constr


class UpdateContributorInsightsRequest(BaseModel):
    """
    Request model for the UpdateContributorInsights operation.

    Attributes
    ----------
    ContributorInsightsAction : str
        Represents the contributor insights action.
    TableName : str
        The name of the table or its ARN.
    IndexName : Optional[str]
        The global secondary index name, if applicable.
    """

    ContributorInsightsAction: Literal["ENABLE", "DISABLE"]
    TableName: constr(min_length=1, max_length=1024)
    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501


class UpdateContributorInsightsResponse(BaseModel):
    """
    Response model for the UpdateContributorInsights operation.

    Attributes
    ----------
    ContributorInsightsStatus : str
        The status of contributor insights.
    IndexName : Optional[str]
        The name of the global secondary index, if applicable.
    TableName : str
        The name of the table.
    """

    ContributorInsightsStatus: Literal[
        "ENABLING", "ENABLED", "DISABLING", "DISABLED", "FAILED"
    ]  # noqa: E501
    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    TableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
