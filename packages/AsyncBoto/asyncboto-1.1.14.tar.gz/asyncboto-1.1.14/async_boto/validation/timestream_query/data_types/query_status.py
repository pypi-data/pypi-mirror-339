from pydantic import BaseModel


class QueryStatus(BaseModel):
    """
    Information about the status of the query, including progress and bytes scanned.

    Parameters
    ----------
    CumulativeBytesMetered : Optional[int], optional
        The amount of data scanned by the query in bytes that you will be charged for.
        This is a cumulative sum and represents the total amount of data that you will
        be charged for since the query was started. The charge is applied only once
        and is either applied when the query completes running or when the query is
        cancelled.
    CumulativeBytesScanned : Optional[int], optional
        The amount of data scanned by the query in bytes. This is a cumulative sum
        and represents the total amount of bytes scanned since the query was started.
    ProgressPercentage : Optional[float], optional
        The progress of the query, expressed as a percentage.
    """

    CumulativeBytesMetered: int | None = None
    CumulativeBytesScanned: int | None = None
    ProgressPercentage: float | None = None
