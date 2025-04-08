from pydantic import BaseModel, conint, constr


class GetLayerVersionPolicyRequest(BaseModel):
    """
    Request model for retrieving the permission policy for a version of an AWS
    Lambda layer.

    Attributes
    ----------
    LayerName : str
        The name or ARN of the layer.
    VersionNumber : int
        The version number.
    """

    LayerName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+)|[a-zA-Z0-9-_]+",  # noqa: E501
    )
    VersionNumber: conint(ge=1)


class GetLayerVersionPolicyResponse(BaseModel):
    """
    Response model for retrieving the permission policy for a version of an AWS
    Lambda layer.

    Attributes
    ----------
    Policy : str
        The policy document.
    RevisionId : str
        A unique identifier for the current revision of the policy.
    """

    Policy: str
    RevisionId: str
