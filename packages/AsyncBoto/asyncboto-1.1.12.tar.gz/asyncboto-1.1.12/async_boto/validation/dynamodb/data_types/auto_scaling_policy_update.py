# ruff: noqa: E501
from pydantic import BaseModel, Field

from .auto_scaling_target_tracking_scaling_policy_configuration_update import (
    AutoScalingTargetTrackingScalingPolicyConfigurationUpdate,
)


class AutoScalingPolicyUpdate(BaseModel):
    r"""
    Represents the auto scaling policy to be modified.

    Attributes
    ----------
    TargetTrackingScalingPolicyConfiguration : AutoScalingTargetTrackingScalingPolicyConfigurationUpdate
        Represents a target tracking scaling policy configuration.
    PolicyName : Optional[str]
        The name of the scaling policy. Minimum length of 1. Maximum length of 256.
        Pattern: \p{Print}+
    """

    TargetTrackingScalingPolicyConfiguration: (
        AutoScalingTargetTrackingScalingPolicyConfigurationUpdate
    )
    PolicyName: str | None = Field(None, min_length=1, max_length=256)
