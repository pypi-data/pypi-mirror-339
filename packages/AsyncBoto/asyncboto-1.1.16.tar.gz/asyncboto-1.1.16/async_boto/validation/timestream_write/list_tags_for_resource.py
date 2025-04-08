from pydantic import BaseModel, constr

from .data_types.tag import Tag


class ListTagsForResourceRequest(BaseModel):
    """
    Lists all tags on a Timestream resource.

    Attributes
    ----------
    ResourceARN : str
        The Timestream resource with tags to be listed.
        This value is an Amazon Resource Name (ARN).
    """

    ResourceARN: constr(min_length=1, max_length=1011)


class ListTagsForResourceResponse(BaseModel):
    """
    The response returned by the service when a ListTagsForResource action is
    successful.

    Attributes
    ----------
    Tags : List[Tag]
        The tags currently associated with the Timestream resource.
    """

    Tags: list[Tag]
