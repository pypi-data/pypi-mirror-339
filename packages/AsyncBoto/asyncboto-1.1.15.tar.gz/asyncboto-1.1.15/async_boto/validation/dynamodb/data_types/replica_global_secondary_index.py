from pydantic import BaseModel, constr

from .on_demand_throughput_override import (
    OnDemandThroughputOverride as OnDemandThroughputOverrideModel,
)
from .provisioned_throughput_override import (
    ProvisionedThroughputOverride as ProvisionedThroughputOverrideModel,
)


class ReplicaGlobalSecondaryIndex(BaseModel):
    """
    Represents the properties of a replica global secondary index.

    Attributes
    ----------
    IndexName : str
        The name of the global secondary index.
    OnDemandThroughputOverride : Optional[OnDemandThroughputOverride]
        Overrides the maximum on-demand throughput settings for the specified global
        secondary index in the specified replica table.
    ProvisionedThroughputOverride : Optional[ProvisionedThroughputOverride]
        Replica table GSI-specific provisioned throughput. If not specified, uses the
        source table GSI's read capacity settings.
    """

    IndexName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    OnDemandThroughputOverride: OnDemandThroughputOverrideModel | None = None
    ProvisionedThroughputOverride: ProvisionedThroughputOverrideModel | None = None
