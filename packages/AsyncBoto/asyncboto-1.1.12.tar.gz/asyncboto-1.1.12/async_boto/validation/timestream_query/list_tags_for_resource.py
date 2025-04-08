from pydantic import BaseModel, Field, constr

from .data_types.tag import Tag


class ListTagsForResourceRequest(BaseModel):
    """
    List all tags on a Timestream query resource.

    Parameters
    ----------
    MaxResults : int
        The maximum number of tags to return.
    NextToken : str
        A pagination token to resume pagination.
    ResourceARN : str
        The Timestream resource with tags to be listed.
        This value is an Amazon Resource Name (ARN).
    """

    MaxResults: int | None = Field(None, ge=1, le=200)
    NextToken: str | None = None
    ResourceARN: constr(min_length=1, max_length=2048)


class ListTagsForResourceResponse(BaseModel):
    """
    The response returned by the service when a ListTagsForResource action is
    successful.

    Parameters
    ----------
    NextToken : str
        A pagination token to resume pagination with a subsequent call
        to ListTagsForResourceResponse.
    Tags : List[Tag]
        The tags currently associated with the Timestream resource.
    """

    NextToken: str | None = None
    Tags: list[Tag] | None = None
