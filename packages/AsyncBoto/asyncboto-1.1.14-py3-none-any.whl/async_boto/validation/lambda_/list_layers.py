from typing import Literal

from pydantic import BaseModel

from .data_types.layers_list_item import LayersListItem


class ListLayersRequest(BaseModel):
    """
    Request model for listing AWS Lambda layers.

    Attributes
    ----------
    CompatibleArchitecture : str
        The compatible instruction set architecture.
    CompatibleRuntime : str
        A runtime identifier.
    Marker : str
        A pagination token returned by a previous call.
    MaxItems : int
        The maximum number of layers to return.
    """

    CompatibleArchitecture: Literal["x86_64", "arm64"] | None
    CompatibleRuntime: (
        Literal[
            "nodejs",
            "nodejs4.3",
            "nodejs6.10",
            "nodejs8.10",
            "nodejs10.x",
            "nodejs12.x",
            "nodejs14.x",
            "nodejs16.x",
            "java8",
            "java8.al2",
            "java11",
            "python2.7",
            "python3.6",
            "python3.7",
            "python3.8",
            "python3.9",
            "dotnetcore1.0",
            "dotnetcore2.0",
            "dotnetcore2.1",
            "dotnetcore3.1",
            "dotnet6",
            "dotnet8",
            "nodejs4.3-edge",
            "go1.x",
            "ruby2.5",
            "ruby2.7",
            "provided",
            "provided.al2",
            "nodejs18.x",
            "python3.10",
            "java17",
            "ruby3.2",
            "ruby3.3",
            "ruby3.4",
            "python3.11",
            "nodejs20.x",
            "provided.al2023",
            "python3.12",
            "java21",
            "python3.13",
            "nodejs22.x",
        ]
        | None
    )
    Marker: str | None
    MaxItems: int | None


class ListLayersResponse(BaseModel):
    """
    Response model for listing AWS Lambda layers.

    Attributes
    ----------
    Layers : list
        A list of function layers.
    NextMarker : str
        A pagination token that's included if more results are available.
    """

    Layers: list[LayersListItem]
    NextMarker: str | None
