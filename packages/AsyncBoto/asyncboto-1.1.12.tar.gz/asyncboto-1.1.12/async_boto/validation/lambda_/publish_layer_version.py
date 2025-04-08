from typing import Literal

from pydantic import BaseModel, constr

from .data_types.layer_version_content_input import LayerVersionContentInput
from .data_types.layer_version_content_output import LayerVersionContentOutput


class PublishLayerVersionRequest(BaseModel):
    """
    Request model for publishing a new version of an AWS Lambda layer.

    Attributes
    ----------
    LayerName : str
        The name or ARN of the layer.
    CompatibleArchitectures : list
        A list of compatible instruction set architectures.
    CompatibleRuntimes : list
        A list of compatible function runtimes.
    Content : LayerVersionContentInput
        The function layer archive.
    Description : str
        The description of the version.
    LicenseInfo : str
        The layer's software license.
    """

    LayerName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+)|[a-zA-Z0-9-_]+",  # noqa: E501
    )
    CompatibleArchitectures: list[Literal["x86_64", "arm64"]] | None
    CompatibleRuntimes: (
        list[
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
        ]
        | None
    )
    Content: LayerVersionContentInput
    Description: constr(max_length=256) | None
    LicenseInfo: constr(max_length=512) | None


class PublishLayerVersionResponse(BaseModel):
    """
    Response model for publishing a new version of an AWS Lambda layer.

    Attributes
    ----------
    CompatibleArchitectures : list
        A list of compatible instruction set architectures.
    CompatibleRuntimes : list
        The layer's compatible runtimes.
    Content : LayerVersionContentOutput
        Details about the layer version.
    CreatedDate : str
        The date that the layer version was created.
    Description : str
        The description of the version.
    LayerArn : str
        The ARN of the layer.
    LayerVersionArn : str
        The ARN of the layer version.
    LicenseInfo : str
        The layer's software license.
    Version : int
        The version number.
    """

    CompatibleArchitectures: list[str] | None
    CompatibleRuntimes: list[str] | None
    Content: LayerVersionContentOutput | None
    CreatedDate: str | None
    Description: str | None
    LayerArn: str | None
    LayerVersionArn: str | None
    LicenseInfo: str | None
    Version: int | None
