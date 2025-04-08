# ruff: noqa: E501
from pydantic import BaseModel

from .magnetic_store_rejected_data_location import (
    MagneticStoreRejectedDataLocation as MagneticStoreRejectedDataLocationModel,
)


class MagneticStoreWriteProperties(BaseModel):
    """
    The set of properties on a table for configuring magnetic store writes.

    Attributes
    ----------
    EnableMagneticStoreWrites : bool
        A flag to enable magnetic store writes.
    MagneticStoreRejectedDataLocation : MagneticStoreRejectedDataLocation | None
        The location to write error reports for records rejected asynchronously during
        magnetic store writes.
    """

    EnableMagneticStoreWrites: bool
    MagneticStoreRejectedDataLocation: MagneticStoreRejectedDataLocationModel | None = (
        None
    )
