from pydantic import BaseModel, Field

from .auto_scaling_policy_description import AutoScalingPolicyDescription


class AutoScalingSettingsDescription(BaseModel):
    """
    Represents the auto scaling settings for a global table or global secondary index.

    Attributes
    ----------
    AutoScalingDisabled : Optional[bool]
        Disabled auto scaling for this global table or global secondary index.
    AutoScalingRoleArn : Optional[str]
        Role ARN used for configuring the auto scaling policy.
    MaximumUnits : Optional[int]
        The maximum capacity units that a global table or global secondary index should
        be scaled up to.
        Valid Range: Minimum value of 1.
    MinimumUnits : Optional[int]
        The minimum capacity units that a global table or global secondary index should
        be scaled down to.
        Valid Range: Minimum value of 1.
    ScalingPolicies : Optional[List[AutoScalingPolicyDescription]]
        Information about the scaling policies.
    """

    AutoScalingDisabled: bool | None = None
    AutoScalingRoleArn: str | None = None
    MaximumUnits: int | None = Field(None, ge=1)
    MinimumUnits: int | None = Field(None, ge=1)
    ScalingPolicies: list[AutoScalingPolicyDescription] | None = None
