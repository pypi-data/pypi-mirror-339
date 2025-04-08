from pydantic import BaseModel, constr


class RemoveLayerVersionPermissionRequest(BaseModel):
    """
    Request model for removing a statement from the permissions policy for a version of
    an AWS Lambda layer.

    Attributes
    ----------
    LayerName : str
        The name or ARN of the layer.
    VersionNumber : int
        The version number.
    StatementId : str
        The identifier that was specified when the statement was added.
    RevisionId : str
        Only update the policy if the revision ID matches the ID specified.
    """

    LayerName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+)|[a-zA-Z0-9-_]+",  # noqa: E501
    )
    VersionNumber: int
    StatementId: constr(min_length=1, max_length=100, pattern=r"([a-zA-Z0-9-_]+)")
    RevisionId: str | None


class RemoveLayerVersionPermissionResponse(BaseModel):
    """
    Response model for removing a statement from the permissions policy for a version
    of an AWS Lambda layer.

    This is an empty response model as the API returns a 204 No Content status.
    """

    pass
