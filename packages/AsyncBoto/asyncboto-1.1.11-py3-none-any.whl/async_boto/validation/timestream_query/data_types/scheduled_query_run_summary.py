# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from .error_report_location import ErrorReportLocation
from .execution_stats import ExecutionStats
from .scheduled_query_insights_response import ScheduledQueryInsightsResponse


class ScheduledQueryRunSummary(BaseModel):
    """
    Run summary for the scheduled query

    Parameters
    ----------
    ErrorReportLocation : Optional[ErrorReportLocation], optional
        S3 location for error report.
    ExecutionStats : Optional[ExecutionStats], optional
        Runtime statistics for a scheduled run.
    FailureReason : Optional[str], optional
        Error message for the scheduled query in case of failure. You might have
        to look at the error report to get more detailed error reasons.
    InvocationTime : Optional[datetime], optional
        InvocationTime for this run. This is the time at which the query is scheduled
        to run. Parameter `@scheduled_runtime` can be used in the query to get the value.
    QueryInsightsResponse : Optional[ScheduledQueryInsightsResponse], optional
        Provides various insights and metrics related to the run summary of the scheduled query.
    RunStatus : Optional[Literal['AUTO_TRIGGER_SUCCESS', 'AUTO_TRIGGER_FAILURE', 'MANUAL_TRIGGER_SUCCESS', 'MANUAL_TRIGGER_FAILURE']], optional
        The status of a scheduled query run.
    TriggerTime : Optional[datetime], optional
        The actual time when the query was run.
    """

    ErrorReportLocation: ErrorReportLocation | None = None
    ExecutionStats: ExecutionStats | None = None
    FailureReason: str | None = None
    InvocationTime: datetime | None = None
    QueryInsightsResponse: ScheduledQueryInsightsResponse | None = None
    RunStatus: (
        Literal[
            "AUTO_TRIGGER_SUCCESS",
            "AUTO_TRIGGER_FAILURE",
            "MANUAL_TRIGGER_SUCCESS",
            "MANUAL_TRIGGER_FAILURE",
        ]
        | None
    ) = None
    TriggerTime: datetime | None = None
