from pydantic import BaseModel, Field, constr

from .data_types.tag import Tag


class TagResourceRequest(BaseModel):
    """
    Associate a set of tags with a Timestream resource. You can then activate these
    user-defined tags so that they appear on the Billing and Cost Management console
    for cost allocation tracking.

    Parameters
    ----------
    ResourceARN : str
        Identifies the Timestream resource to which tags should be added.
        This value is an Amazon Resource Name (ARN).
    Tags : List[Tag]
        The tags to be assigned to the Timestream resource.
    """

    ResourceARN: constr(min_length=1, max_length=2048)
    Tags: list[Tag] = Field(..., min_length=0, max_length=200)


class TagResourceResponse(BaseModel):
    """
    The response returned by the service when a TagResource action is successful.
    If the action is successful, the service sends back an HTTP 200 response
    with an empty HTTP body.
    """

    pass
