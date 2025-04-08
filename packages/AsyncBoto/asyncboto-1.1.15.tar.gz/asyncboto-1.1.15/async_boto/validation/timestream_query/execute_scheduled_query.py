from pydantic import BaseModel, constr

from .data_types.scheduled_query_insights import ScheduledQueryInsights


class ExecuteScheduledQueryRequest(BaseModel):
    """
    You can use this API to run a scheduled query manually.

    If you enabled QueryInsights, this API also returns insights and metrics
    related to the query that you executed as part of an Amazon SNS notification.
    QueryInsights helps with performance tuning of your query.

    Parameters
    ----------
    ClientToken : str
        Not used.
    InvocationTime : int
        The timestamp in UTC. Query will be run as if it was invoked at this timestamp.
    QueryInsights : ScheduledQueryInsights
        Encapsulates settings for enabling QueryInsights.
    ScheduledQueryArn : str
        ARN of the scheduled query.
    """

    ClientToken: constr(min_length=32, max_length=128) | None = None
    InvocationTime: int
    QueryInsights: ScheduledQueryInsights | None = None
    ScheduledQueryArn: constr(min_length=1, max_length=2048)


class ExecuteScheduledQueryResponse(BaseModel):
    """
    The response returned by the service when an ExecuteScheduledQuery action is
    successful.
    If the action is successful, the service sends back an HTTP 200 response with
    an empty HTTP body.
    """

    pass
