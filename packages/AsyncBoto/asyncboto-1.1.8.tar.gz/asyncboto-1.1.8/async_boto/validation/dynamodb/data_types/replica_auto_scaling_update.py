# ruff: noqa: E501
from pydantic import BaseModel, constr

from .auto_scaling_settings_update import AutoScalingSettingsUpdate
from .replica_global_secondary_index_auto_scaling_update import (
    ReplicaGlobalSecondaryIndexAutoScalingUpdate,
)


class ReplicaAutoScalingUpdate(BaseModel):
    """
    Represents the auto scaling settings of a replica that will be modified.

    Attributes
    ----------
    RegionName : str
        The Region where the replica exists.
    ReplicaGlobalSecondaryIndexUpdates : Optional[List[ReplicaGlobalSecondaryIndexAutoScalingUpdate]]
        Represents the auto scaling settings of global secondary indexes that will be modified.
    ReplicaProvisionedReadCapacityAutoScalingUpdate : Optional[AutoScalingSettingsUpdate]
        Represents the auto scaling settings to be modified for a global table or global secondary index.
    """

    RegionName: constr(min_length=1)
    ReplicaGlobalSecondaryIndexUpdates: (
        list[ReplicaGlobalSecondaryIndexAutoScalingUpdate] | None
    ) = None
    ReplicaProvisionedReadCapacityAutoScalingUpdate: (
        AutoScalingSettingsUpdate | None
    ) = None
