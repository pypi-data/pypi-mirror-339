from pydantic import BaseModel, constr


class UntagResourceRequest(BaseModel):
    """
    Removes the association of tags from a Timestream resource.

    Attributes
    ----------
    ResourceARN : str
        The Timestream resource that the tags will be removed from.
        This value is an Amazon Resource Name (ARN).
    TagKeys : List[str]
        A list of tag keys. Existing tags of the resource whose keys are members
        of this list will be removed from the Timestream resource.
    """

    ResourceARN: constr(min_length=1, max_length=1011)
    TagKeys: list[constr(min_length=1, max_length=128)]


class UntagResourceResponse(BaseModel):
    """
    The response returned by the service when an UntagResource action is successful.
    """

    pass
