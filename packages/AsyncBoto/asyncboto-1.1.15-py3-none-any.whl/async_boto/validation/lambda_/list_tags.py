from pydantic import BaseModel, constr


class ListTagsRequest(BaseModel):
    """
    Request model for listing tags of a Lambda resource.

    Attributes
    ----------
    ARN : str
        The resource's Amazon Resource Name (ARN).
    """

    ARN: constr(
        min_length=1,
        max_length=256,
        pattern=r"arn:(aws[a-zA-Z-]*):lambda:[a-z]{2}((-gov)|(-iso([a-z]?)))?-[a-z]+-\d{1}:\d{12}:(function:[a-zA-Z0-9-_]+(:(\$LATEST|[a-zA-Z0-9-_]+))?|code-signing-config:csc-[a-z0-9]{17}|event-source-mapping:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
    )


class ListTagsResponse(BaseModel):
    """
    Response model for listing tags of a Lambda resource.

    Attributes
    ----------
    Tags : dict
        The function's tags.
    """

    Tags: dict[str, str]
