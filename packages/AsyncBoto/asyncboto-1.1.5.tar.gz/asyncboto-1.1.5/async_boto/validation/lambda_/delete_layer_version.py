from pydantic import BaseModel, constr


class DeleteLayerVersionRequest(BaseModel):
    """
    Request model for deleting a version of a Lambda layer.

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
        pattern=r"(arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+)|[a-zA-Z0-9-_]+",
    )
    VersionNumber: int


class DeleteLayerVersionResponse(BaseModel):
    """
    Response model for deleting a version of a Lambda layer.

    This is an empty response model as the API returns a 204 No Content status.
    """

    pass
