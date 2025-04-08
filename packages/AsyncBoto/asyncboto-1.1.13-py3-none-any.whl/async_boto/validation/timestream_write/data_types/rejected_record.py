from pydantic import BaseModel, conint


class RejectedRecord(BaseModel):
    """
    Represents records that were not successfully inserted into Timestream
    due to data validation issues.

    Attributes
    ----------
    ExistingVersion : int | None
        The existing version of the record.
    Reason : str | None
        The reason why a record was not successfully inserted into Timestream.
    RecordIndex : int | None
        The index of the record in the input request for WriteRecords.
    """

    ExistingVersion: conint(ge=1) | None = None
    Reason: str | None = None
    RecordIndex: int | None = None
