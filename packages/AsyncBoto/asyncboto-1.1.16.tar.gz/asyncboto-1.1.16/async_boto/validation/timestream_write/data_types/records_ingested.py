from pydantic import BaseModel


class RecordsIngested(BaseModel):
    """
    Information on the records ingested by this request.

    Attributes
    ----------
    MagneticStore : int | None
        Count of records ingested into the magnetic store.
    MemoryStore : int | None
        Count of records ingested into the memory store.
    Total : int | None
        Total count of successfully ingested records.
    """

    MagneticStore: int | None = None
    MemoryStore: int | None = None
    Total: int | None = None
