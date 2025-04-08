from typing import Literal

from pydantic import BaseModel, constr

from .data_types.update_kinesis_streaming_configuration import (
    UpdateKinesisStreamingConfiguration as UpdateKinesisStreamingConfigurationModel,
)


class UpdateKinesisStreamingDestinationRequest(BaseModel):
    """
    Request model for the UpdateKinesisStreamingDestination operation.

    Attributes
    ----------
    StreamArn : constr(min_length=37, max_length=1024)
        The Amazon Resource Name (ARN) for the Kinesis stream input.
    TableName : constr(min_length=1, max_length=1024)
        The table name for the Kinesis streaming destination input.
    UpdateKinesisStreamingConfiguration : Optional[UpdateKinesisStreamingConfiguration]
        The command to update the Kinesis stream configuration.
    """

    StreamArn: constr(min_length=37, max_length=1024)
    TableName: constr(min_length=1, max_length=1024)
    UpdateKinesisStreamingConfiguration: (
        UpdateKinesisStreamingConfigurationModel | None
    ) = None  # noqa: E501


class UpdateKinesisStreamingDestinationResponse(BaseModel):
    """
    Response model for the UpdateKinesisStreamingDestination operation.

    Attributes
    ----------
    DestinationStatus : Literal["ENABLING", "ACTIVE", "DISABLING", "DISABLED",
                                "ENABLE_FAILED", "UPDATING"]
        The status of the attempt to update the Kinesis streaming destination output.
    StreamArn : constr(min_length=37, max_length=1024)
        The ARN for the Kinesis stream input.
    TableName : constr(min_length=3, max_length=255, regex=r'[a-zA-Z0-9_.-]+')
        The table name for the Kinesis streaming destination output.
    UpdateKinesisStreamingConfiguration : UpdateKinesisStreamingConfigurationModel
        optional
        The command to update the Kinesis streaming destination configuration.
    """

    DestinationStatus: Literal[
        "ENABLING", "ACTIVE", "DISABLING", "DISABLED", "ENABLE_FAILED", "UPDATING"
    ]
    StreamArn: constr(min_length=37, max_length=1024)
    TableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    UpdateKinesisStreamingConfiguration: (
        UpdateKinesisStreamingConfigurationModel | None
    ) = None  # noqa: E501
