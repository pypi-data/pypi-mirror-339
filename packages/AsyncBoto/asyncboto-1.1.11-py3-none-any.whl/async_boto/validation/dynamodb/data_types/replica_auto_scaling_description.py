# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr

from .auto_scaling_settings_description import AutoScalingSettingsDescription
from .replica_global_secondary_index_auto_scaling_description import (
    ReplicaGlobalSecondaryIndexAutoScalingDescription,
)


class ReplicaAutoScalingDescription(BaseModel):
    """
    Represents the auto scaling settings of the replica.

    Attributes
    ----------
    GlobalSecondaryIndexes : Optional[List[ReplicaGlobalSecondaryIndexAutoScalingDescription]]
        Replica-specific global secondary index auto scaling settings.
    RegionName : Optional[str]
        The Region where the replica exists.
    ReplicaProvisionedReadCapacityAutoScalingSettings : Optional[AutoScalingSettingsDescription]
        Represents the auto scaling settings for a global table or global secondary index.
    ReplicaProvisionedWriteCapacityAutoScalingSettings : Optional[AutoScalingSettingsDescription]
        Represents the auto scaling settings for a global table or global secondary index.
    ReplicaStatus : Optional[str]
        The current state of the replica.
    """

    GlobalSecondaryIndexes: (
        list[ReplicaGlobalSecondaryIndexAutoScalingDescription] | None
    ) = None
    RegionName: constr(min_length=1) | None = None
    ReplicaProvisionedReadCapacityAutoScalingSettings: (
        AutoScalingSettingsDescription | None
    ) = None
    ReplicaProvisionedWriteCapacityAutoScalingSettings: (
        AutoScalingSettingsDescription | None
    ) = None
    ReplicaStatus: (
        Literal[
            "CREATING",
            "CREATION_FAILED",
            "UPDATING",
            "DELETING",
            "ACTIVE",
            "REGION_DISABLED",
            "INACCESSIBLE_ENCRYPTION_CREDENTIALS",
        ]
        | None
    ) = None
