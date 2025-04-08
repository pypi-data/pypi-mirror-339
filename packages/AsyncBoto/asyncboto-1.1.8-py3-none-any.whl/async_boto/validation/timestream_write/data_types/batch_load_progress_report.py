from pydantic import BaseModel


class BatchLoadProgressReport(BaseModel):
    """
    Details about the progress of a batch load task.

    Attributes
    ----------
    BytesMetered : int | None
        The number of bytes metered.
    FileFailures : int | None
        The number of file failures.
    ParseFailures : int | None
        The number of parse failures.
    RecordIngestionFailures : int | None
        The number of record ingestion failures.
    RecordsIngested : int | None
        The number of records ingested.
    RecordsProcessed : int | None
        The number of records processed.
    """

    BytesMetered: int | None = None
    FileFailures: int | None = None
    ParseFailures: int | None = None
    RecordIngestionFailures: int | None = None
    RecordsIngested: int | None = None
    RecordsProcessed: int | None = None
