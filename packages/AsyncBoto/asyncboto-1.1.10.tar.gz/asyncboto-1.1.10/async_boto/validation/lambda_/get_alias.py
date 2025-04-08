from pydantic import BaseModel, constr

from .data_types.alias_routing_configuration import AliasRoutingConfiguration


class GetAliasRequest(BaseModel):
    """
    Request model for retrieving details about a Lambda function alias.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    Name : str
        The name of the alias.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",
    )
    Name: constr(min_length=1, max_length=128)


class GetAliasResponse(BaseModel):
    """
    Response model for retrieving details about a Lambda function alias.

    Attributes
    ----------
    AliasArn : str
        The Amazon Resource Name (ARN) of the alias.
    Description : str
        A description of the alias.
    FunctionVersion : str
        The function version that the alias invokes.
    Name : str
        The name of the alias.
    RevisionId : str
        A unique identifier that changes when you update the alias.
    RoutingConfig : AliasRoutingConfiguration
        The routing configuration of the alias.
    """

    AliasArn: constr(
        pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}(-gov)?-[a-z]+-\d{1}:\d{12}:function:[a-zA-Z0-9-_]+(:(\$LATEST|[a-zA-Z0-9-_]+))?"
    )
    Description: constr(min_length=0, max_length=256) | None
    FunctionVersion: constr(min_length=1, max_length=1024)
    Name: constr(min_length=1, max_length=128)
    RevisionId: str | None
    RoutingConfig: AliasRoutingConfiguration | None
