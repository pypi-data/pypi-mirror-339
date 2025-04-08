from pydantic import BaseModel, constr

from .data_types.tag import Tag


class TagResourceRequest(BaseModel):
    """
    Request model for the TagResource operation.

    Attributes
    ----------
    ResourceArn : str
        Identifies the Amazon DynamoDB resource to which tags should be added.
    Tags : List[Tag]
        The tags to be assigned to the Amazon DynamoDB resource.
    """

    ResourceArn: constr(min_length=1, max_length=1283)
    Tags: list[Tag]


class TagResourceResponse(BaseModel):
    """
    Response model for the TagResource operation.

    This model represents an empty response body for a successful operation.
    """
