from typing import Literal

from pydantic import BaseModel


class CodeSigningPolicies(BaseModel):
    """
    Code signing configuration policies for Lambda function deployment validation.

    Specifies the validation failure action for signature mismatch or expiry during
    Lambda function deployment.

    Parameters
    ----------
    UntrustedArtifactOnDeployment : Optional[Literal["Warn", "Enforce"]]
        Defines the action to take when a code signature validation check fails during
        deployment.

        Available options:
        - "Warn": Lambda allows the deployment to proceed but logs a warning.
                This is useful
                 for testing or transition periods, as it won't block deployments with
                 invalid
                 signatures but provides visibility into signature issues.
        - "Enforce": Lambda blocks the deployment request if signature validation
        checks fail.
                    This provides the strongest security posture by preventing any
                    unsigned or
                    invalidly signed code from being deployed.

        Default value: "Warn"
    """

    UntrustedArtifactOnDeployment: Literal["Warn", "Enforce"] | None = None
