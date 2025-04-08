from pydantic import BaseModel, constr

from .auto_scaling_settings_update import AutoScalingSettingsUpdate


class ReplicaGlobalSecondaryIndexAutoScalingUpdate(BaseModel):
    """
    Represents the auto scaling settings of a global secondary index for a replica
    that will be modified.

    Attributes
    ----------
    IndexName : Optional[str]
        The name of the global secondary index.
    ProvisionedReadCapacityAutoScalingUpdate : Optional[AutoScalingSettingsUpdate]
        Represents the auto scaling settings to be modified for a global table or
        global secondary index.
    """

    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    ProvisionedReadCapacityAutoScalingUpdate: AutoScalingSettingsUpdate | None = None
