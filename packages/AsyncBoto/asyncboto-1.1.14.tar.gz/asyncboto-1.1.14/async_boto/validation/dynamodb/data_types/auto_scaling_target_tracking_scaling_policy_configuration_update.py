from pydantic import BaseModel, Field


class AutoScalingTargetTrackingScalingPolicyConfigurationUpdate(BaseModel):
    TargetValue: float = Field(..., ge=8.515920e-109, le=1.174271e108)
    DisableScaleIn: bool | None = False
    ScaleInCooldown: int | None = None
    ScaleOutCooldown: int | None = None
