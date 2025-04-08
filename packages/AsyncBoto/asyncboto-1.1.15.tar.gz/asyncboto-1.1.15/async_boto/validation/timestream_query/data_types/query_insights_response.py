from pydantic import BaseModel

from .query_spatial_coverage import QuerySpatialCoverage
from .query_temporal_range import QueryTemporalRange


class QueryInsightsResponse(BaseModel):
    """
    Provides various insights and metrics related to the query that you executed.

    Parameters
    ----------
    OutputBytes : Optional[int]
        Indicates the size of query result set in bytes. You can use this data to
        validate if the result set has changed as part of the query tuning exercise.
    OutputRows : Optional[int]
        Indicates the total number of rows returned as part of the query result set.
        You can use this data to validate if the number of rows in the result set
        have changed as part of the query tuning exercise.
    QuerySpatialCoverage : Optional[QuerySpatialCoverage]
        Provides insights into the spatial coverage of the query, including the table
        with sub-optimal (max) spatial pruning. This information can help you identify
        areas for improvement in your partitioning strategy to enhance spatial pruning.
    QueryTableCount : Optional[int]
        Indicates the number of tables in the query.
    QueryTemporalRange : Optional[QueryTemporalRange]
        Provides insights into the temporal range of the query, including the table with
        the largest (max) time range. Following are some of the potential options for
        optimizing time-based pruning:
        * Add missing time-predicates.
        * Remove functions around the time predicates.
        * Add time predicates to all the sub-queries.
    UnloadPartitionCount : Optional[int]
        Indicates the partitions created by the `Unload` operation.
    UnloadWrittenBytes : Optional[int]
        Indicates the size, in bytes, written by the `Unload` operation.
    UnloadWrittenRows : Optional[int]
        Indicates the rows written by the `Unload` query.
    """

    OutputBytes: int | None = None
    OutputRows: int | None = None
    QuerySpatialCoverage: QuerySpatialCoverage | None = None
    QueryTableCount: int | None = None
    QueryTemporalRange: QueryTemporalRange | None = None
    UnloadPartitionCount: int | None = None
    UnloadWrittenBytes: int | None = None
    UnloadWrittenRows: int | None = None
