from typing import Literal

from pydantic import BaseModel, conint, constr

from .auto_scaling_settings_update import AutoScalingSettingsUpdate
from .replica_global_secondary_index_settings_update import (
    ReplicaGlobalSecondaryIndexSettingsUpdate as ReplicaGlobalSecondaryIndexSettingsUpdateModel,  # noqa: E501
)


class ReplicaSettingsUpdate(BaseModel):
    """
    Represents the settings for a global table in a Region that will be modified.

    Attributes
    ----------
    RegionName : str
        The Region of the replica to be added.
    ReplicaGlobalSecondaryIndexSettingsUpdate : Optional[List[
        ReplicaGlobalSecondaryIndexSettingsUpdate]]
        Represents the settings of a global secondary index for a global table
         that will be modified.
    ReplicaProvisionedReadCapacityAutoScalingSettingsUpdate : AutoScalingSettingsUpdate
        Auto scaling settings for managing a global table replica's read capacity units.
    ReplicaProvisionedReadCapacityUnits : Optional[int]
        The maximum number of strongly consistent reads consumed per second before
        DynamoDB returns a ThrottlingException.
    ReplicaTableClass : Optional[str]
        Replica-specific table class. If not specified, uses the source table's table
        class.
    """

    RegionName: constr(min_length=1)
    ReplicaGlobalSecondaryIndexSettingsUpdate: (
        list[ReplicaGlobalSecondaryIndexSettingsUpdateModel] | None
    ) = None  # noqa: E501
    ReplicaProvisionedReadCapacityAutoScalingSettingsUpdate: (
        AutoScalingSettingsUpdate | None
    ) = None  # noqa: E501
    ReplicaProvisionedReadCapacityUnits: conint(ge=1) | None = None
    ReplicaTableClass: Literal["STANDARD", "STANDARD_INFREQUENT_ACCESS"] | None = None
