from pydantic import BaseModel

from .timestream_configuration import TimestreamConfiguration


class TargetConfiguration(BaseModel):
    """
    Configuration used for writing the output of a query.

    Parameters
    ----------
    TimestreamConfiguration : TimestreamConfiguration
        Configuration needed to write data into the Timestream database and table.
    """

    TimestreamConfiguration: TimestreamConfiguration
