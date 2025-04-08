from typing import Literal

from pydantic import BaseModel


class EnableKinesisStreamingConfiguration(BaseModel):
    """
    Enables setting the configuration for Kinesis Streaming.

    Attributes
    ----------
    ApproximateCreationDateTimePrecision : Literal["MILLISECOND", "MICROSECOND"],
    optional
        Toggle for the precision of Kinesis data stream timestamp.
        The values are either MILLISECOND or MICROSECOND.
    """

    ApproximateCreationDateTimePrecision: (
        Literal["MILLISECOND", "MICROSECOND"] | None
    ) = None  # noqa: E501
