from pydantic import BaseModel, conint


class OnDemandThroughputOverride(BaseModel):
    """
    Overrides the on-demand throughput settings for this replica table.

    Attributes
    ----------
    MaxReadRequestUnits : Optional[int]
        Maximum number of read request units for the specified replica table.
    """

    MaxReadRequestUnits: conint(ge=-1) | None = None
