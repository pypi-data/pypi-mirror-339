from pydantic import BaseModel, conint, constr

from .auto_scaling_settings_update import AutoScalingSettingsUpdate


class ReplicaGlobalSecondaryIndexSettingsUpdate(BaseModel):
    """
    Represents the settings of a global secondary index for a global table that will
    be modified.

    Attributes
    ----------
    IndexName : str
        The name of the global secondary index. The name must be unique among all
        other indexes on this table.
    ProvisionedReadCapacityAutoScalingSettingsUpdate : Optional[AutoScalingSettings
    Update]
        Auto scaling settings for managing a global secondary index replica's read
        capacity units.
    ProvisionedReadCapacityUnits : Optional[int]
        The maximum number of strongly consistent reads consumed per second before
        DynamoDB returns a ThrottlingException.
    """

    IndexName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    ProvisionedReadCapacityAutoScalingSettingsUpdate: (
        AutoScalingSettingsUpdate | None
    ) = None  # noqa: E501
    ProvisionedReadCapacityUnits: conint(ge=1) | None = None
