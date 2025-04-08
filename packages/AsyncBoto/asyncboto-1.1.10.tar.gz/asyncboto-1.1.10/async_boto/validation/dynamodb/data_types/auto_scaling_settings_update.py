from pydantic import BaseModel, Field

from .auto_scaling_policy_update import AutoScalingPolicyUpdate


class AutoScalingSettingsUpdate(BaseModel):
    """
    Represents the auto scaling settings to be modified for a global table or global
    secondary index.

    Attributes
    ----------
    AutoScalingDisabled : Optional[bool]
        Disabled auto scaling for this global table or global secondary index.
    AutoScalingRoleArn : Optional[str]
        Role ARN used for configuring auto scaling policy. Minimum length of 1.
        Maximum length of 1600.
    MaximumUnits : Optional[int]
        The maximum capacity units that a global table or global secondary index should
         be scaled up to.
        Valid Range: Minimum value of 1.
    MinimumUnits : Optional[int]
        The minimum capacity units that a global table or global secondary index
        should be scaled down to.
        Valid Range: Minimum value of 1.
    ScalingPolicyUpdate : Optional[AutoScalingPolicyUpdate]
        The scaling policy to apply for scaling target global table or global secondary
        index capacity units.
    """

    AutoScalingDisabled: bool | None = None
    AutoScalingRoleArn: str | None = Field(
        None,
        min_length=1,
        max_length=1600,
    )
    MaximumUnits: int | None = Field(None, ge=1)
    MinimumUnits: int | None = Field(None, ge=1)
    ScalingPolicyUpdate: AutoScalingPolicyUpdate | None = None
