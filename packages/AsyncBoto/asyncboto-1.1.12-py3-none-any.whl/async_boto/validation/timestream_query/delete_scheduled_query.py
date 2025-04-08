from pydantic import BaseModel, constr


class DeleteScheduledQueryRequest(BaseModel):
    """
    Deletes a given scheduled query. This is an irreversible operation.

    Parameters
    ----------
    ScheduledQueryArn : str
        The ARN of the scheduled query.
    """

    ScheduledQueryArn: constr(min_length=1, max_length=2048)


class DeleteScheduledQueryResponse(BaseModel):
    """
    The response returned by the service when a DeleteScheduledQuery action is
    successful.
    If the action is successful, the service sends back an HTTP 200 response with an
    empty HTTP body.
    """

    pass
