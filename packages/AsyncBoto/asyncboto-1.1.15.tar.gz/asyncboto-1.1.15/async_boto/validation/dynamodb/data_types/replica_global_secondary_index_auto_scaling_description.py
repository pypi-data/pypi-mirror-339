# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr

from .auto_scaling_settings_description import AutoScalingSettingsDescription


class ReplicaGlobalSecondaryIndexAutoScalingDescription(BaseModel):
    """
    Represents the auto scaling configuration for a replica global secondary index.

    Attributes
    ----------
    IndexName : Optional[str]
        The name of the global secondary index.
    IndexStatus : Optional[str]
        The current state of the replica global secondary index.
    ProvisionedReadCapacityAutoScalingSettings : Optional[AutoScalingSettingsDescription]
        Represents the auto scaling settings for a global table or global secondary index.
    ProvisionedWriteCapacityAutoScalingSettings : Optional[AutoScalingSettingsDescription]
        Represents the auto scaling settings for a global table or global secondary index.
    """

    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    IndexStatus: Literal["CREATING", "UPDATING", "DELETING", "ACTIVE"] | None = None
    ProvisionedReadCapacityAutoScalingSettings: (
        AutoScalingSettingsDescription | None
    ) = None  # noqa: E501
    ProvisionedWriteCapacityAutoScalingSettings: (
        AutoScalingSettingsDescription | None
    ) = None  # noqa: E501
