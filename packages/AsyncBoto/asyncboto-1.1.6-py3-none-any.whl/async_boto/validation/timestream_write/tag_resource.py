from pydantic import BaseModel, constr

from .data_types.tag import Tag


class TagResourceRequest(BaseModel):
    """
    Associates a set of tags with a Timestream resource.

    Attributes
    ----------
    ResourceARN : str
        Identifies the Timestream resource to which tags should be added.
        This value is an Amazon Resource Name (ARN).
    Tags : List[Tag]
        The tags to be assigned to the Timestream resource.
    """

    ResourceARN: constr(min_length=1, max_length=1011)
    Tags: list[Tag]


class TagResourceResponse(BaseModel):
    """
    The response returned by the service when a TagResource action is successful.
    """

    pass
