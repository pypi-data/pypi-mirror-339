from pydantic import BaseModel, constr

from .data_types.auto_scaling_settings_update import AutoScalingSettingsUpdate
from .data_types.global_secondary_index_auto_scaling_update import (
    GlobalSecondaryIndexAutoScalingUpdate,
)
from .data_types.replica_auto_scaling_update import ReplicaAutoScalingUpdate
from .data_types.table_auto_scaling_description import (
    TableAutoScalingDescription as TableAutoScalingDescriptionModel,
)


class UpdateTableReplicaAutoScalingRequest(BaseModel):
    """
    Request model for the UpdateTableReplicaAutoScaling operation.

    Attributes
    ----------
    TableName : constr(min_length=1, max_length=1024)
        The name of the global table to be updated.
    GlobalSecondaryIndexUpdates : Optional[List[GlobalSecondaryIndexAutoScalingUpdate]]
        Represents the auto scaling settings of the global secondary indexes of the
        replica to be updated.
    ProvisionedWriteCapacityAutoScalingUpdate : Optional[AutoScalingSettingsUpdate]
        Represents the auto scaling settings to be modified for a global table or
        global secondary index.
    ReplicaUpdates : Optional[List[ReplicaAutoScalingUpdate]]
        Represents the auto scaling settings of replicas of the table that will be
        modified.
    """

    TableName: constr(min_length=1, max_length=1024)
    GlobalSecondaryIndexUpdates: list[GlobalSecondaryIndexAutoScalingUpdate] | None = (
        None  # noqa: E501
    )
    ProvisionedWriteCapacityAutoScalingUpdate: AutoScalingSettingsUpdate | None = None
    ReplicaUpdates: list[ReplicaAutoScalingUpdate] | None = None


class UpdateTableReplicaAutoScalingResponse(BaseModel):
    """
    Response model for the UpdateTableReplicaAutoScaling operation.

    Attributes
    ----------
    TableAutoScalingDescription : Optional[TableAutoScalingDescription]
        Returns information about the auto scaling settings of a table with replicas.
    """

    TableAutoScalingDescription: TableAutoScalingDescriptionModel | None = None
