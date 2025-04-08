from typing import Literal

from pydantic import BaseModel


class UpdateKinesisStreamingConfiguration(BaseModel):
    """
    Enables updating the configuration for Kinesis Streaming.

    Attributes
    ----------
    ApproximateCreationDateTimePrecision : Literal['MILLISECOND','MICROSECOND']
        Enables updating the precision of Kinesis data stream timestamp.
    """

    ApproximateCreationDateTimePrecision: (
        Literal["MILLISECOND", "MICROSECOND"] | None
    ) = None  # noqa: E501
