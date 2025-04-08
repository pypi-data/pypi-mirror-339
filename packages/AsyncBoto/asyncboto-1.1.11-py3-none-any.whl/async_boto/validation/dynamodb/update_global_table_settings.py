# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr

from .data_types.auto_scaling_settings_update import AutoScalingSettingsUpdate
from .data_types.global_table_global_secondary_index_settings_update import (
    GlobalTableGlobalSecondaryIndexSettingsUpdate as GlobalTableGlobalSecondaryIndexSettingsUpdateModel,
)
from .data_types.replica_settings_description import ReplicaSettingsDescription
from .data_types.replica_settings_update import (
    ReplicaSettingsUpdate as ReplicaSettingsUpdateModel,
)


class UpdateGlobalTableSettingsRequest(BaseModel):
    """
    Request model for the UpdateGlobalTableSettings operation.

    Attributes
    ----------
    GlobalTableName : str
        The name of the global table.
    GlobalTableBillingMode : Optional[str]
        The billing mode of the global table.
    GlobalTableGlobalSecondaryIndexSettingsUpdate : Optional[List[GlobalTableGlobalSecondaryIndexSettingsUpdate]]
        The settings of a global secondary index for a global table that will be modified.
    GlobalTableProvisionedWriteCapacityAutoScalingSettingsUpdate : AutoScalingSettingsUpdate
        Auto scaling settings for managing provisioned write capacity for the global
        table.
    GlobalTableProvisionedWriteCapacityUnits : Optional[int]
        The maximum number of writes consumed per second before DynamoDB returns a
        ThrottlingException.
    ReplicaSettingsUpdate : Optional[List[ReplicaSettingsUpdate]]
        The settings for a global table in a Region that will be modified.
    """

    GlobalTableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    GlobalTableBillingMode: Literal["PROVISIONED", "PAY_PER_REQUEST"] | None = None
    GlobalTableGlobalSecondaryIndexSettingsUpdate: (
        list[GlobalTableGlobalSecondaryIndexSettingsUpdateModel] | None
    ) = None  # noqa: E501
    GlobalTableProvisionedWriteCapacityAutoScalingSettingsUpdate: (
        AutoScalingSettingsUpdate | None
    ) = None  # noqa: E501
    GlobalTableProvisionedWriteCapacityUnits: int | None = None
    ReplicaSettingsUpdate: list[ReplicaSettingsUpdateModel] | None = None


class UpdateGlobalTableSettingsResponse(BaseModel):
    """
    Response model for the UpdateGlobalTableSettings operation.

    Attributes
    ----------
    GlobalTableName : str
        The name of the global table.
    ReplicaSettings : List[ReplicaSettingsDescription]
        The Region-specific settings for the global table.
    """

    GlobalTableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    ReplicaSettings: list[ReplicaSettingsDescription]
