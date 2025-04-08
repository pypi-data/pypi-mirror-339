from pydantic import BaseModel, constr


class UntagResourceRequest(BaseModel):
    """
    Request model for the UntagResource operation.

    Attributes
    ----------
    ResourceArn : str
        The DynamoDB resource that the tags will be removed from.
    TagKeys : List[str]
        A list of tag keys to be removed.
    """

    ResourceArn: constr(min_length=1, max_length=1283)
    TagKeys: list[constr(min_length=1, max_length=128)]


class UntagResourceResponse(BaseModel):
    """
    Response model for the UntagResource operation.

    This model represents an empty response body for a successful operation.
    """

    pass
