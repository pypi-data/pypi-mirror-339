from pydantic import BaseModel

from .query_spatial_coverage_max import QuerySpatialCoverageMax


class QuerySpatialCoverage(BaseModel):
    """
    Provides insights into the spatial coverage of the query, including the
    table with sub-optimal (max) spatial pruning.

    This information can help identify areas for improvement in partitioning
    strategy to enhance spatial pruning.

    Examples
    --------
    With the `QuerySpatialCoverage` information, you can:
    * Add measure_name or use customer-defined partition key (CDPK) predicates.
    * If you've already done the preceding action, remove functions around
      them or clauses, such as `LIKE`.
    """

    Max: QuerySpatialCoverageMax | None = None
