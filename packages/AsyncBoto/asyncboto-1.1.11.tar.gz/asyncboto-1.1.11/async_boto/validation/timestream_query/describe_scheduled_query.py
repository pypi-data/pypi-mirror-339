from pydantic import BaseModel, constr

from .data_types.scheduled_query_description import ScheduledQueryDescription


class DescribeScheduledQueryRequest(BaseModel):
    """
    Provides detailed information about a scheduled query.

    Parameters
    ----------
    ScheduledQueryArn : str
        The ARN of the scheduled query.
    """

    ScheduledQueryArn: constr(min_length=1, max_length=2048)


class DescribeScheduledQueryResponse(BaseModel):
    """
    The response returned by the service when a
    DescribeScheduledQuery action is successful.

    Parameters
    ----------
    ScheduledQuery : ScheduledQueryDescription
        The scheduled query.
    """

    ScheduledQuery: ScheduledQueryDescription
