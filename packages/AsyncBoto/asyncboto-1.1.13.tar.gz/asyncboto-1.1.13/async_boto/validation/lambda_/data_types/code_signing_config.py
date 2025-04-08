from pydantic import BaseModel, Field

from .allowed_publishers import AllowedPublishers
from .code_signing_policies import CodeSigningPolicies


class CodeSigningConfig(BaseModel):
    r"""
    Details about a Code signing configuration for Lambda functions.

    A code signing configuration defines a list of allowed signing profiles
    and defines the code-signing validation policy (action to be taken if
    deployment validation checks fail).

    Parameters
    ----------
    AllowedPublishers : AllowedPublishers
        List of allowed publishers (signing profiles) that can sign a code package.
        When a user tries to deploy a code package, Lambda validates that the code
        package
        has been signed by one of these trusted publishers.

    CodeSigningConfigArn : str
        The Amazon Resource Name (ARN) of the Code signing configuration.
        Format: arn:aws:lambda:[region]:[account-id]:code-signing-config:csc-[id]

    CodeSigningConfigId : str
        Unique identifier for the Code signing configuration.
        Format: csc-[a-zA-Z0-9-_\.]{17}

    CodeSigningPolicies : CodeSigningPolicies
        The code signing policy controls the validation failure action for
        signature mismatch or expiry.

    LastModified : str
        The date and time that the Code signing configuration was last modified,
        in ISO-8601 format (YYYY-MM-DDThh:mm:ss.sTZD).

    Description : Optional[str]
        Code signing configuration description to help identify its purpose.
        Maximum length: 256 characters
    """

    AllowedPublishers: AllowedPublishers
    CodeSigningConfigArn: str
    CodeSigningConfigId: str
    CodeSigningPolicies: CodeSigningPolicies
    LastModified: str
    Description: str | None = Field(None, min_length=0, max_length=256)
