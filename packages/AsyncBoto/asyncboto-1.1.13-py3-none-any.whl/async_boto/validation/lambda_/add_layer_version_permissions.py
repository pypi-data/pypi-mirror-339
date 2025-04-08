from pydantic import BaseModel, constr


class AddLayerVersionPermissionRequest(BaseModel):
    """
    Request model for the AddLayerVersionPermission operation.

    Adds permissions to the resource-based policy of a version of an AWS Lambda layer.

    Attributes
    ----------
    LayerName : str
        The name or Amazon Resource Name (ARN) of the layer.
    VersionNumber : int
        The version number.
    RevisionId : Optional[str]
        Only update the policy if the revision ID matches the ID specified.
    Action : str
        The API action that grants access to the layer. For example,
        lambda:GetLayerVersion.
    OrganizationId : Optional[str]
        With the principal set to *, grant permission to all accounts in the specified
        organization.
    Principal : str
        An account ID, or * to grant layer usage permission to all accounts in an
        organization, or all AWS accounts.
    StatementId : str
        An identifier that distinguishes the policy from others on the same layer
        version.
    """

    LayerName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+)|[a-zA-Z0-9-_]+",
    )
    VersionNumber: int
    RevisionId: str | None = None
    Action: constr(max_length=22, pattern=r"lambda:GetLayerVersion")
    OrganizationId: constr(max_length=34, pattern=r"o-[a-z0-9]{10,32}") | None = None
    Principal: constr(pattern=r"\d{12}|\*|arn:(aws[a-zA-Z-]*):iam::\d{12}:root")
    StatementId: constr(min_length=1, max_length=100, pattern=r"([a-zA-Z0-9-_]+)")


class AddLayerVersionPermissionResponse(BaseModel):
    """
    Response model for the AddLayerVersionPermission operation.

    Attributes
    ----------
    RevisionId : str
        A unique identifier for the current revision of the policy.
    Statement : str
        The permission statement.
    """

    RevisionId: str
    Statement: str
