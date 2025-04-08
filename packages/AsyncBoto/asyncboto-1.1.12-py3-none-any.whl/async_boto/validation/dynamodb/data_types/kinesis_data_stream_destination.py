# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr


class KinesisDataStreamDestination(BaseModel):
    """
    Describes a Kinesis data stream destination.

    Attributes
    ----------
    ApproximateCreationDateTimePrecision : Optional[Literal['MILLISECOND', 'MICROSECOND']]
        The precision of the Kinesis data stream timestamp.
    DestinationStatus : Optional[Literal['ENABLING', 'ACTIVE', 'DISABLING', 'DISABLED', 'ENABLE_FAILED', 'UPDATING']]
        The current status of replication.
    DestinationStatusDescription : Optional[str]
        The human-readable string that corresponds to the replica status.
    StreamArn : Optional[constr(min_length=37, max_length=1024)]
        The ARN for a specific Kinesis data stream.
    """

    ApproximateCreationDateTimePrecision: (
        Literal["MILLISECOND", "MICROSECOND"] | None
    ) = None  # noqa: E501
    DestinationStatus: (
        Literal[
            "ENABLING", "ACTIVE", "DISABLING", "DISABLED", "ENABLE_FAILED", "UPDATING"
        ]
        | None
    ) = None  # noqa: E501
    DestinationStatusDescription: str | None = None
    StreamArn: constr(min_length=37, max_length=1024) | None = None
