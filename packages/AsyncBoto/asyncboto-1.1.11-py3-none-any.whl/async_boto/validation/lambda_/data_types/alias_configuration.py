# ruff: noqa: E501
from pydantic import BaseModel, Field

from .alias_routing_configuration import AliasRoutingConfiguration


class AliasConfiguration(BaseModel):
    """
    Provides configuration information about a Lambda function alias.

    An alias is a named resource that maps to a function version and can be used
    to route traffic between different versions.

    Parameters
    ----------
    AliasArn : Optional[str]
        The Amazon Resource Name (ARN) of the alias. Uniquely identifies the alias.
        Format: arn:aws:lambda:[region]:[account-id]:function:[function-name]:[alias-name]
    Description : Optional[str]
        A description of the alias that helps identify its purpose or configuration.
        Maximum length: 256 characters.
    FunctionVersion : Optional[str]
        The function version that the alias invokes when called.
        Can be a version number or "$LATEST" for the unpublished version.
    Name : Optional[str]
        The name of the alias. Used as an identifier and can be referenced in API calls.
    RevisionId : Optional[str]
        A unique identifier that changes when you update the alias.
        Used for optimistic locking to prevent concurrent modifications.
    RoutingConfig : Optional[AliasRoutingConfiguration]
        The routing configuration of the alias, which allows traffic splitting
        between two function versions.
    """

    AliasArn: str | None = None
    Description: str | None = Field(None, min_length=0, max_length=256)
    FunctionVersion: str | None = None
    Name: str | None = None
    RevisionId: str | None = None
    RoutingConfig: AliasRoutingConfiguration | None = None
