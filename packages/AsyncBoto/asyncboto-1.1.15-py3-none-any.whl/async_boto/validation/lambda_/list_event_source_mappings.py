from pydantic import BaseModel, constr

from .data_types.event_source_mapping_configuration import (
    EventSourceMappingConfiguration,
)


class ListEventSourceMappingsRequest(BaseModel):
    """
    Request model for listing event source mappings.

    Attributes
    ----------
    EventSourceArn : str
        The Amazon Resource Name (ARN) of the event source.
    FunctionName : str
        The name or ARN of the Lambda function.
    Marker : str
        A pagination token returned by a previous call.
    MaxItems : int
        The maximum number of event source mappings to return.
    """

    EventSourceArn: (
        constr(pattern=r"arn:(aws[a-zA-Z0-9-]*):([a-zA-Z0-9\-])+:(\d{12})?:(.*)") | None
    )
    FunctionName: (
        constr(
            min_length=1,
            max_length=140,
            pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
        )
        | None
    )
    Marker: str | None
    MaxItems: int | None


class ListEventSourceMappingsResponse(BaseModel):
    """
    Response model for listing event source mappings.

    Attributes
    ----------
    EventSourceMappings : list
        A list of event source mappings.
    NextMarker : str
        A pagination token that's included if more results are available.
    """

    EventSourceMappings: list[EventSourceMappingConfiguration]
    NextMarker: str | None
