from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr

from .data_types.failure_exception import FailureException as FailureExceptionModel


class DescribeContributorInsightsRequest(BaseModel):
    """
    Returns information about contributor insights for a given table or global
    secondary index.

    Attributes
    ----------
    TableName : str
        The name of the table to describe. You can also provide the Amazon Resource Name
         (ARN) of the table in this parameter.
    IndexName : Optional[str]
        The name of the global secondary index to describe, if applicable.
    """

    TableName: constr(min_length=1, max_length=1024)
    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501


class DescribeContributorInsightsResponse(BaseModel):
    """
    Response for the DescribeContributorInsights operation.

    Attributes
    ----------
    TableName : str
        The name of the table being described.
    IndexName : Optional[str]
        The name of the global secondary index being described, if applicable.
    ContributorInsightsStatus : str
        The current status of contributor insights.
    LastUpdateDateTime : Optional[datetime]
        The last time contributor insights were updated.
    FailureException : Optional[FailureException]
        The failure details, if any.
    ContributorInsightsRuleList : List[str]
        List of names of the associated contributor insights rules.
    """

    TableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    ContributorInsightsStatus: Literal[
        "ENABLING", "ENABLED", "DISABLING", "DISABLED", "FAILED"
    ]
    LastUpdateDateTime: datetime | None = None
    FailureException: FailureExceptionModel | None = None
    ContributorInsightsRuleList: (
        list[constr(pattern=r"[A-Za-z0-9][A-Za-z0-9\-\_\.]{0,126}[A-Za-z0-9]")] | None
    ) = None  # noqa: E501
