from pydantic import BaseModel

from .query_spatial_coverage import QuerySpatialCoverage
from .query_temporal_range import QueryTemporalRange


class ScheduledQueryInsightsResponse(BaseModel):
    """
    Provides various insights and metrics related to the `ExecuteScheduledQueryRequest`
    that was executed.

    Parameters
    ----------
    OutputBytes : Optional[int], optional
        Indicates the size of query result set in bytes. You can use this data to
        validate if the result set has changed as part of the query tuning exercise.
    OutputRows : Optional[int], optional
        Indicates the total number of rows returned as part of the query result set.
        You can use this data to validate if the number of rows in the result set
        have changed as part of the query tuning exercise.
    QuerySpatialCoverage : Optional[QuerySpatialCoverage], optional
        Provides insights into the spatial coverage of the query, including the
        table with sub-optimal (max) spatial pruning. This information can help
        you identify areas for improvement in your partitioning strategy to
        enhance spatial pruning.
    QueryTableCount : Optional[int], optional
        Indicates the number of tables in the query.
    QueryTemporalRange : Optional[QueryTemporalRange], optional
        Provides insights into the temporal range of the query, including the
        table with the largest (max) time range. Following are some of the
        potential options for optimizing time-based pruning:
        * Add missing time-predicates.
        * Remove functions around the time predicates.
        * Add time predicates to all the sub-queries.
    """

    OutputBytes: int | None = None
    OutputRows: int | None = None
    QuerySpatialCoverage: QuerySpatialCoverage | None = None
    QueryTableCount: int | None = None
    QueryTemporalRange: QueryTemporalRange | None = None
