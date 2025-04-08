from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr

from .on_demand_throughput_override import (
    OnDemandThroughputOverride as OnDemandThroughputOverrideModel,
)
from .provisioned_throughput_override import (
    ProvisionedThroughputOverride as ProvisionedThroughputOverrideModel,
)
from .replica_global_secondary_index_description import (
    ReplicaGlobalSecondaryIndexDescription,
)
from .table_class_summary import TableClassSummary
from .table_warm_throughput_description import TableWarmThroughputDescription


class ReplicaDescription(BaseModel):
    """
    Contains the details of the replica.

    Attributes
    ----------
    GlobalSecondaryIndexes : Optional[List[ReplicaGlobalSecondaryIndexDescription]]
        Replica-specific global secondary index settings.
    KMSMasterKeyId : Optional[str]
        The AWS KMS key of the replica that will be used for AWS KMS encryption.
    OnDemandThroughputOverride : Optional[OnDemandThroughputOverride]
        Overrides the maximum on-demand throughput settings for the specified replica
        table.
    ProvisionedThroughputOverride : Optional[ProvisionedThroughputOverride]
        Replica-specific provisioned throughput. If not described, uses the source
        table's provisioned throughput settings.
    RegionName : Optional[str]
        The name of the Region.
    ReplicaInaccessibleDateTime : Optional[datetime]
        The time at which the replica was first detected as inaccessible.
    ReplicaStatus : Optional[str]
        The current state of the replica.
    ReplicaStatusDescription : Optional[str]
        Detailed information about the replica status.
    ReplicaStatusPercentProgress : Optional[str]
        Specifies the progress of a Create, Update, or Delete action on the replica as
        a percentage.
    ReplicaTableClassSummary : Optional[TableClassSummary]
        Contains details of the table class.
    WarmThroughput : Optional[TableWarmThroughputDescription]
        Represents the warm throughput value for this replica.
    """

    GlobalSecondaryIndexes: list[ReplicaGlobalSecondaryIndexDescription] | None = None
    KMSMasterKeyId: str | None = None
    OnDemandThroughputOverride: OnDemandThroughputOverrideModel | None = None
    ProvisionedThroughputOverride: ProvisionedThroughputOverrideModel | None = None
    RegionName: constr(min_length=1) | None = None
    ReplicaInaccessibleDateTime: datetime | None = None
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
    ReplicaStatusDescription: str | None = None
    ReplicaStatusPercentProgress: str | None = None
    ReplicaTableClassSummary: TableClassSummary | None = None
    WarmThroughput: TableWarmThroughputDescription | None = None
