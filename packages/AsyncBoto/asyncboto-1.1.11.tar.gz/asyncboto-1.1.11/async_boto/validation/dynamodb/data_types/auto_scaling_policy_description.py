# ruff: noqa: E501
from pydantic import BaseModel, Field

from .auto_scaling_target_tracking_scaling_policy_configuration_description import (
    AutoScalingTargetTrackingScalingPolicyConfigurationDescription,
)


class AutoScalingPolicyDescription(BaseModel):
    PolicyName: str | None = Field(None, min_length=1, max_length=256)
    TargetTrackingScalingPolicyConfiguration: (
        AutoScalingTargetTrackingScalingPolicyConfigurationDescription | None
    ) = None
