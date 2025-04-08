from pydantic import BaseModel


class ProvisionedPollerConfig(BaseModel):
    """
    The provisioned mode configuration for the event source.

    An event poller is a compute unit that provides approximately 5 MBps of throughput.

    Attributes
    ----------
    MaximumPollers : Optional[int]
        The maximum number of event pollers this event source can scale up to.
    MinimumPollers : Optional[int]
        The minimum number of event pollers this event source can scale down to.
    """

    MaximumPollers: int | None = None
    MinimumPollers: int | None = None
