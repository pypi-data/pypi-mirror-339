from pydantic import BaseModel, constr

from .on_demand_throughput import OnDemandThroughput as OnDemandThroughputModel
from .provisioned_throughput import ProvisionedThroughput as ProvisionedThroughputModel
from .warm_throughput import WarmThroughput as WarmThroughputModel


class UpdateGlobalSecondaryIndexAction(BaseModel):
    """
    Represents the new provisioned throughput settings to be applied to a global
    secondary index.

    Attributes
    ----------
    IndexName : constr(min_length=3, max_length=255, regex='[a-zA-Z0-9_.-]+')
        The name of the global secondary index to be updated.
    OnDemandThroughput : Optional[OnDemandThroughput]
        Updates the maximum number of read and write units for the specified
        global secondary index.
    ProvisionedThroughput : Optional[ProvisionedThroughput]
        Represents the provisioned throughput settings for the specified global
        secondary index.
    WarmThroughput : Optional[WarmThroughput]
        Represents the warm throughput value of the new provisioned throughput settings
        to be applied to a global secondary index.
    """

    IndexName: constr(min_length=3, max_length=255, pattern="[a-zA-Z0-9_.-]+")
    OnDemandThroughput: OnDemandThroughputModel | None = None
    ProvisionedThroughput: ProvisionedThroughputModel | None = None
    WarmThroughput: WarmThroughputModel | None = None
