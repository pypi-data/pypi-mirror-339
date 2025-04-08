from pydantic import BaseModel, constr

from .auto_scaling_settings_update import AutoScalingSettingsUpdate


class GlobalSecondaryIndexAutoScalingUpdate(BaseModel):
    """
    Represents the auto scaling settings of a global secondary index for a global table
    that will be modified.

    Attributes
    ----------
    IndexName : Optional[constr(min_length=3, max_length=255, regex=r'[a-zA-Z0-9_.-]+')]
        The name of the global secondary index.
    ProvisionedWriteCapacityAutoScalingUpdate : Optional[AutoScalingSettingsUpdate]
        Represents the auto scaling settings to be modified for a global table or global
         secondary index.
    """

    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    ProvisionedWriteCapacityAutoScalingUpdate: AutoScalingSettingsUpdate | None = None
