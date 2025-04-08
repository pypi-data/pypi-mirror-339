from pydantic import BaseModel, constr


class TagResourceRequest(BaseModel):
    """
    Request model for adding tags to a function, event source mapping, or code signing
    configuration.

    Attributes
    ----------
    ARN : str
        The resource's Amazon Resource Name (ARN).
    Tags : Dict[str, str]
        A list of tags to apply to the resource.
    """

    ARN: constr(
        min_length=1,
        max_length=256,
        pattern=r"arn:(aws[a-zA-Z-]*):lambda:[a-z]{2}((-gov)|(-iso([a-z]?)))?-[a-z]+-\d{1}:\d{12}:(function:[a-zA-Z0-9-_]+(:(\$LATEST|[a-zA-Z0-9-_]+))?|code-signing-config:csc-[a-z0-9]{17}|event-source-mapping:[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",  # noqa: E501
    )
    Tags: dict[str, str]


class TagResourceResponse(BaseModel):
    """
    Response model for adding tags to a function, event source mapping, or code
    signing configuration.

    This is an empty response model as the API returns a 204 No Content status.
    """

    pass
