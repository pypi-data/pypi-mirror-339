from pydantic import BaseModel


class EventSourceMappingMetricsConfig(BaseModel):
    """
    The metrics configuration for your event source.

    Parameters
    ----------
    Metrics : Optional[List[str]]
        The metrics you want your event source mapping to produce.
    """

    Metrics: list[str] | None = None
