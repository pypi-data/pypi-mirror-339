from enum import Enum

from pydantic import BaseModel


class QueryInsightsMode(str, Enum):
    """
    Modes to enable or disable QueryInsights.
    """

    ENABLED_WITH_RATE_CONTROL = "ENABLED_WITH_RATE_CONTROL"
    DISABLED = "DISABLED"


class QueryInsights(BaseModel):
    """
    A performance tuning feature that helps optimize queries, reducing costs and
    improving performance.

    QueryInsights helps assess pruning efficiency and identify areas for improvement.
    It analyzes
    the effectiveness of queries in terms of temporal and spatial pruning, and
    identifies opportunities to improve performance.

    Key metrics provided are QuerySpatialCoverage and QueryTemporalRange.
    QuerySpatialCoverage
    indicates how much of the spatial axis the query scans, with lower values being
    more efficient.
    QueryTemporalRange shows the time range scanned, with narrower ranges being more
    performant.

    The maximum number of Query API requests allowed with QueryInsights enabled is
    1 query per second (QPS). Exceeding this rate might result in throttling.

    Parameters
    ----------
    Mode : QueryInsightsMode
        The mode that controls whether QueryInsights is enabled or disabled.
    """

    Mode: QueryInsightsMode
