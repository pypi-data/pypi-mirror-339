from pydantic import BaseModel, conint, constr

from .data_types.layer_version_content_output import LayerVersionContentOutput


class GetLayerVersionRequest(BaseModel):
    """
    Request model for retrieving information about a version of an AWS Lambda layer.

    Attributes
    ----------
    LayerName : str
        The name or ARN of the layer.
    VersionNumber : int
        The version number.
    """

    LayerName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+)|[a-zA-Z0-9-_]+",  # noqa: E501
    )
    VersionNumber: conint(ge=1)


class GetLayerVersionResponse(BaseModel):
    """
    Response model for retrieving information about a version of an AWS Lambda layer.

    Attributes
    ----------
    CompatibleArchitectures : List[str]
        A list of compatible instruction set architectures.
    CompatibleRuntimes : List[str]
        The layer's compatible runtimes.
    Content : LayerVersionContentOutput
        Details about the layer version.
    CreatedDate : str
        The date that the layer version was created, in ISO-8601 format.
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
    LayerArn: (
        constr(
            min_length=1,
            max_length=140,
            pattern=r"arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+",
        )
        | None
    )
    LayerVersionArn: (
        constr(
            min_length=1,
            max_length=140,
            pattern=r"arn:[a-zA-Z0-9-]+:lambda:[a-zA-Z0-9-]+:\d{12}:layer:[a-zA-Z0-9-_]+:[0-9]+",  # noqa: E501
        )
        | None
    )
    LicenseInfo: str | None
    Version: int | None
