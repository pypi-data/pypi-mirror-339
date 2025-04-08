from pydantic import BaseModel, conint


class RetentionProperties(BaseModel):
    """
    Retention properties contain the duration for which your time-series
    data must be stored in the magnetic store and the memory store.

    Attributes
    ----------
    MagneticStoreRetentionPeriodInDays : int
        The duration for which data must be stored in the magnetic store.
    MemoryStoreRetentionPeriodInHours : int
        The duration for which data must be stored in the memory store.
    """

    MagneticStoreRetentionPeriodInDays: conint(ge=1, le=73000)
    MemoryStoreRetentionPeriodInHours: conint(ge=1, le=8766)
