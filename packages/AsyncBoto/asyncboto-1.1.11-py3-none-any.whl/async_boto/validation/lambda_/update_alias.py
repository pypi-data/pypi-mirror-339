from pydantic import BaseModel, constr

from .data_types.alias_routing_configuration import AliasRoutingConfiguration


class UpdateAliasRequest(BaseModel):
    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Name: constr(min_length=1, max_length=128)
    Description: constr(min_length=0, max_length=256) | None
    FunctionVersion: constr(min_length=1, max_length=1024) | None
    RevisionId: str | None
    RoutingConfig: AliasRoutingConfiguration | None


class UpdateAliasResponse(BaseModel):
    AliasArn: constr(
        pattern=r"arn:(aws[a-zA-Z-]*)?:lambda:[a-z]{2}(-gov)?-[a-z]+-\d{1}:\d{12}:function:[a-zA-Z0-9-_]+(:(\$LATEST|[a-zA-Z0-9-_]+))?"  # noqa: E501
    )
    Description: constr(min_length=0, max_length=256) | None
    FunctionVersion: constr(min_length=1, max_length=1024)
    Name: constr(min_length=1, max_length=128)
    RevisionId: str | None
    RoutingConfig: AliasRoutingConfiguration | None
