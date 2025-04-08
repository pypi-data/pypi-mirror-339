from pydantic import BaseModel, constr

from .data_types.allowed_publishers import AllowedPublishers
from .data_types.code_signing_config import CodeSigningConfig
from .data_types.code_signing_policies import CodeSigningPolicies


class UpdateCodeSigningConfigRequest(BaseModel):
    CodeSigningConfigArn: constr(
        max_length=200,
        pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}((-gov)|(-iso(b?)))?-[a-z]+-\d{1}:\d{12}:code-signing-config:csc-[a-z0-9]{17}",
    )
    AllowedPublishers: AllowedPublishers | None
    CodeSigningPolicies: CodeSigningPolicies | None
    Description: constr(min_length=0, max_length=256) | None


class UpdateCodeSigningConfigResponse(BaseModel):
    CodeSigningConfig: CodeSigningConfig
