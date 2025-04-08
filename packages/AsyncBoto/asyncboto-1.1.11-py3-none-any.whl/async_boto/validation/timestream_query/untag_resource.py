# ruff: noqa: E501
from pydantic import BaseModel, Field, constr


class UntagResourceRequest(BaseModel):
    """
    Removes the association of tags from a Timestream query resource.

    Parameters
    ----------
    ResourceARN : str
        The Timestream resource that the tags will be removed from.
        This value is an Amazon Resource Name (ARN).
    TagKeys : List[str]
        A list of tags keys. Existing tags of the resource whose
        keys are members of this list
        will be removed from the Timestream resource.
    """

    ResourceARN: constr(min_length=1, max_length=2048)
    TagKeys: list[constr(min_length=1, max_length=128)] = Field(
        ..., min_length=0, max_length=200
    )


class UntagResourceResponse(BaseModel):
    """
    The response returned by the service when an UntagResource action is successful.
    If the action is successful, the service sends back an HTTP 200 response with an
    empty HTTP body.
    """

    pass
