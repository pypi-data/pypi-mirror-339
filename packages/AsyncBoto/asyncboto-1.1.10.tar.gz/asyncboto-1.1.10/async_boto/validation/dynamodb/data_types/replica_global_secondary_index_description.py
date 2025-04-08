from pydantic import BaseModel, constr

from .global_secondary_index_warm_throughput_description import (
    GlobalSecondaryIndexWarmThroughputDescription,
)
from .on_demand_throughput_override import (
    OnDemandThroughputOverride as OnDemandThroughputOverrideModel,
)
from .provisioned_throughput_override import (
    ProvisionedThroughputOverride as ProvisionedThroughputOverrideModel,
)


class ReplicaGlobalSecondaryIndexDescription(BaseModel):
    """
    Represents the properties of a replica global secondary index.

    Attributes
    ----------
    IndexName : Optional[str]
        The name of the global secondary index.
    OnDemandThroughputOverride : Optional[OnDemandThroughputOverride]
        Overrides the maximum on-demand throughput for the specified global secondary
        index in the specified replica table.
    ProvisionedThroughputOverride : Optional[ProvisionedThroughputOverride]
        If not described, uses the source table GSI's read capacity settings.
    WarmThroughput : Optional[GlobalSecondaryIndexWarmThroughputDescription]
        Represents the warm throughput of the global secondary index for this replica.
    """

    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    OnDemandThroughputOverride: OnDemandThroughputOverrideModel | None = None
    ProvisionedThroughputOverride: ProvisionedThroughputOverrideModel | None = None
    WarmThroughput: GlobalSecondaryIndexWarmThroughputDescription | None = None
