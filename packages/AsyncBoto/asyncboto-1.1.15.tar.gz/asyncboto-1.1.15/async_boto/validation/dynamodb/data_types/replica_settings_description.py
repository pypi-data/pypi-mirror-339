from typing import Literal

from pydantic import BaseModel, conint, constr

from .auto_scaling_settings_description import AutoScalingSettingsDescription
from .billing_mode_summary import BillingModeSummary
from .replica_global_secondary_index_settings_description import (
    ReplicaGlobalSecondaryIndexSettingsDescription,
)
from .table_class_summary import TableClassSummary


class ReplicaSettingsDescription(BaseModel):
    """
    Represents the properties of a replica.

    Attributes
    ----------
    RegionName : str
        The Region name of the replica.
    ReplicaBillingModeSummary : Optional[BillingModeSummary]
        The read/write capacity mode of the replica.
    ReplicaGlobalSecondaryIndexSettings : Optional[List[ReplicaGlobalSecondaryIndex
    SettingsDescription]]
        Replica global secondary index settings for the global table.
    ReplicaProvisionedReadCapacityAutoScalingSettings : Optional[
    AutoScalingSettingsDescription]
        Auto scaling settings for a global table replica's read capacity units.
    ReplicaProvisionedReadCapacityUnits : Optional[int]
        The maximum number of strongly consistent reads consumed per second before
        DynamoDB returns a ThrottlingException.
    ReplicaProvisionedWriteCapacityAutoScalingSettings : AutoScalingSettingsDescription
        Auto scaling settings for a global table replica's write capacity units.
    ReplicaProvisionedWriteCapacityUnits : Optional[int]
        The maximum number of writes consumed per second before DynamoDB returns
         a ThrottlingException.
    ReplicaStatus : Optional[str]
        The current state of the Region.
    ReplicaTableClassSummary : Optional[TableClassSummary]
        Contains details of the table class.
    """

    RegionName: constr(min_length=1)
    ReplicaBillingModeSummary: BillingModeSummary | None = None
    ReplicaGlobalSecondaryIndexSettings: (
        list[ReplicaGlobalSecondaryIndexSettingsDescription] | None
    ) = None  # noqa: E501
    ReplicaProvisionedReadCapacityAutoScalingSettings: (
        AutoScalingSettingsDescription | None
    ) = None  # noqa: E501
    ReplicaProvisionedReadCapacityUnits: conint(ge=0) | None = None
    ReplicaProvisionedWriteCapacityAutoScalingSettings: (
        AutoScalingSettingsDescription | None
    ) = None  # noqa: E501
    ReplicaProvisionedWriteCapacityUnits: conint(ge=0) | None = None
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
    ) = None  # noqa: E501
    ReplicaTableClassSummary: TableClassSummary | None = None
