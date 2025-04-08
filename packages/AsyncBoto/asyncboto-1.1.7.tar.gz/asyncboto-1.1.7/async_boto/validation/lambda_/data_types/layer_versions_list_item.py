from typing import Literal

from pydantic import BaseModel


class LayerVersionsListItem(BaseModel):
    """
    Details about a version of an AWS Lambda layer.

    Attributes
    ----------
    CompatibleArchitectures : Optional[List[Literal['x86_64', 'arm64']]]
        A list of compatible instruction set architectures.
    CompatibleRuntimes : Optional[List[Literal[
        'nodejs', 'nodejs4.3', 'nodejs6.10', 'nodejs8.10', 'nodejs10.x',
        'nodejs12.x', 'nodejs14.x', 'nodejs16.x', 'java8', 'java8.al2', 'java11',
        'python2.7', 'python3.6', 'python3.7', 'python3.8', 'python3.9',
        'dotnetcore1.0', 'dotnetcore2.0', 'dotnetcore2.1', 'dotnetcore3.1',
        'dotnet6', 'dotnet8', 'nodejs4.3-edge', 'go1.x', 'ruby2.5', 'ruby2.7',
        'provided', 'provided.al2', 'nodejs18.x', 'python3.10', 'java17',
        'ruby3.2', 'ruby3.3', 'python3.11', 'nodejs20.x', 'provided.al2023',
        'python3.12', 'java21', 'python3.13', 'nodejs22.x'
    ]]]
        The layer's compatible runtimes.
    CreatedDate : Optional[str]
        The date that the version was created, in ISO 8601 format.
    Description : Optional[str]
        The description of the version.
    LayerVersionArn : Optional[str]
        The ARN of the layer version.
    LicenseInfo : Optional[str]
        The layer's open-source license.
    Version : Optional[int]
        The version number.
    """

    CompatibleArchitectures: list[Literal["x86_64", "arm64"]] | None = None
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
    ) = None
    CreatedDate: str | None = None
    Description: str | None = None
    LayerVersionArn: str | None = None
    LicenseInfo: str | None = None
    Version: int | None = None
