from pydantic import BaseModel, constr

from .data_types.enable_kinesis_streaming_configuration import (
    EnableKinesisStreamingConfiguration as EnableKinesisStreamingConfigurationModel,
)


class DisableKinesisStreamingDestinationRequest(BaseModel):
    """
    Stops replication from the DynamoDB table to the Kinesis data stream.

    Attributes
    ----------
    StreamArn : str
        The ARN for a Kinesis data stream.
    TableName : str
        The name of the DynamoDB table. You can also provide the Amazon Resource Name
        (ARN) of the table in this parameter.
    EnableKinesisStreamingConfiguration : Optional[EnableKinesisStreamingConfiguration]
        The source for the Kinesis streaming information that is being enabled.
    """

    StreamArn: constr(min_length=37, max_length=1024)
    TableName: constr(min_length=1, max_length=1024)
    EnableKinesisStreamingConfiguration: (
        EnableKinesisStreamingConfigurationModel | None
    ) = None  # noqa: E501


class DisableKinesisStreamingDestinationResponse(BaseModel):
    """
    Response for the DisableKinesisStreamingDestination operation.

    Attributes
    ----------
    DestinationStatus : Optional[str]
        The current status of the replication.
    EnableKinesisStreamingConfiguration : EnableKinesisStreamingConfigurationModel
        The destination for the Kinesis streaming information that is being enabled.
    StreamArn : Optional[str]
        The ARN for the specific Kinesis data stream.
    TableName : Optional[str]
        The name of the table being modified.
    """

    DestinationStatus: str | None = None
    EnableKinesisStreamingConfiguration: (
        EnableKinesisStreamingConfigurationModel | None
    ) = None  # noqa: E501
    StreamArn: constr(min_length=37, max_length=1024) | None = None
    TableName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
