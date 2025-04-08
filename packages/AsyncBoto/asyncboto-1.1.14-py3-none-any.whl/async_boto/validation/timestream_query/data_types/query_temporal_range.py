from pydantic import BaseModel

from .query_temporal_range_max import QueryTemporalRangeMax


class QueryTemporalRange(BaseModel):
    """
    Provides insights into the temporal range of the query, including the table
    with the largest (max) time range.

    Parameters
    ----------
    Max : Optional[QueryTemporalRangeMax], optional
        Encapsulates the following properties that provide insights into the most
        sub-optimal performing table on the temporal axis:
        * `Value` – The maximum duration in nanoseconds between the start and end
          of the query.
        * `TableArn` – The Amazon Resource Name (ARN) of the table which is queried
          with the largest time range.
    """

    Max: QueryTemporalRangeMax | None = None
