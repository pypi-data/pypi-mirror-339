from pydantic import BaseModel, constr


class CancelQueryRequest(BaseModel):
    """
    Cancels a query that has been issued. Cancellation is provided only if the query
    has not
    completed running before the cancellation request was issued. Because cancellation
    is an idempotent operation, subsequent cancellation requests will return a
    `CancellationMessage`,
    indicating that the query has already been canceled.

    Attributes
    ----------
    QueryId : str
        The ID of the query that needs to be cancelled. `QueryID` is returned as part
        of the query result.
    """

    QueryId: constr(min_length=1, max_length=64, pattern=r"[a-zA-Z0-9]+")


class CancelQueryResponse(BaseModel):
    """
    The response returned by the service when a CancelQuery action is successful.

    Attributes
    ----------
    CancellationMessage : str | None
        A `CancellationMessage` is returned when a `CancelQuery` request for the
        query specified
        by `QueryId` has already been issued.
    """

    CancellationMessage: str | None = None
