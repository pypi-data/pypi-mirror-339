from typing import Literal

from pydantic import BaseModel, constr


class UpdateScheduledQueryRequest(BaseModel):
    """
    Update a scheduled query.

    Parameters
    ----------
    ScheduledQueryArn : str
        ARN of the scheduled query.
    State : str
        State of the scheduled query.
    """

    ScheduledQueryArn: constr(min_length=1, max_length=2048)
    State: Literal["ENABLED", "DISABLED"]


class UpdateScheduledQueryResponse(BaseModel):
    """
    The response returned by the service when an UpdateScheduledQuery action
    is successful.
    If the action is successful, the service sends back an HTTP 200 response
    with an empty HTTP body.
    """

    pass
