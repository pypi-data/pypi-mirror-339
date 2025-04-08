# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr


class ContributorInsightsSummary(BaseModel):
    """
    Represents a Contributor Insights summary entry.

    Attributes
    ----------
    ContributorInsightsStatus : Optional[Literal["ENABLING", "ENABLED", "DISABLING", "DISABLED", "FAILED"]]
        Describes the current status for contributor insights for the given table and index, if applicable.
    IndexName : Optional[constr(min_length=3, max_length=255, regex=r"[a-zA-Z0-9_.-]+")]
        Name of the index associated with the summary, if any.
    TableName : Optional[constr(min_length=3, max_length=255, regex=r"[a-zA-Z0-9_.-]+")]
        Name of the table associated with the summary.
    """

    ContributorInsightsStatus: (
        Literal["ENABLING", "ENABLED", "DISABLING", "DISABLED", "FAILED"] | None
    ) = None
    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None
    TableName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None
