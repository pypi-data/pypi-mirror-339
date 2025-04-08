from pydantic import BaseModel, constr

from .data_types.tag import Tag


class ListTagsOfResourceRequest(BaseModel):
    """
    Request model for the ListTagsOfResource operation.

    Attributes
    ----------
    ResourceArn : str
        The Amazon DynamoDB resource with tags to be listed.
    NextToken : Optional[str]
        An optional string that, if supplied, must be copied from the output of a
        previous call to ListTagsOfResource.
    """

    ResourceArn: constr(min_length=1, max_length=1283)
    NextToken: str | None = None


class ListTagsOfResourceResponse(BaseModel):
    """
    Response model for the ListTagsOfResource operation.

    Attributes
    ----------
    NextToken : Optional[str]
        If this value is returned, there are additional results to be displayed.
    Tags : Optional[List[Tag]]
        The tags currently associated with the Amazon DynamoDB resource.
    """

    NextToken: constr(min_length=1, max_length=1024) | None = None
    Tags: list[Tag] | None = None
