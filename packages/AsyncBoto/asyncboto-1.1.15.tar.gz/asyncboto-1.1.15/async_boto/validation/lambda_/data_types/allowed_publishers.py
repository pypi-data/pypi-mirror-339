# ruff: noqa: E501
from pydantic import BaseModel


class AllowedPublishers(BaseModel):
    """
    List of signing profiles that can sign a code package for a Lambda function.

    Used as part of a code signing configuration to specify which signing profiles
    are trusted to sign code packages that can be deployed to Lambda functions.

    Parameters
    ----------
    SigningProfileVersionArns : List[str]
        The Amazon Resource Names (ARNs) for each of the signing profiles.
        A signing profile defines a trusted user who can sign a code package.
        Each ARN uniquely identifies a specific version of a signing profile.

        Format: arn:aws:signer:[region]:[account-id]:signing-profile:[profile-name]/[version]

        Lambda verifies that code packages are signed by one of these trusted
        profiles before deploying them to functions that use this code signing
        configuration.

        Minimum items: 1
        Maximum items: 20
    """

    SigningProfileVersionArns: list[str]
