from pydantic import BaseModel, Field


class QueryTemporalRangeMax(BaseModel):
    """
    Provides insights into the table with the most sub-optimal temporal pruning
    scanned by your query.

    Parameters
    ----------
    TableArn : Optional[str], optional
        The Amazon Resource Name (ARN) of the table which is queried with the
        largest time range.
    Value : Optional[int], optional
        The maximum duration in nanoseconds between the start and end of the query.
    """

    TableArn: str | None = Field(None, min_length=1, max_length=2048)
    Value: int | None = None
