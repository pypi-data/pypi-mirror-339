from pydantic import BaseModel


class ExecutionStats(BaseModel):
    """
    Statistics for a single scheduled query run.

    Parameters
    ----------
    BytesMetered : Optional[int]
        Bytes metered for a single scheduled query run.
    CumulativeBytesScanned : Optional[int]
        Bytes scanned for a single scheduled query run.
    DataWrites : Optional[int]
        Data writes metered for records ingested in a single scheduled query run.
    ExecutionTimeInMillis : Optional[int]
        Total time, measured in milliseconds, that was needed for the scheduled
        query run to complete.
    QueryResultRows : Optional[int]
        Number of rows present in the output from running a query before ingestion
        to destination data source.
    RecordsIngested : Optional[int]
        The number of records ingested for a single scheduled query run.
    """

    BytesMetered: int | None = None
    CumulativeBytesScanned: int | None = None
    DataWrites: int | None = None
    ExecutionTimeInMillis: int | None = None
    QueryResultRows: int | None = None
    RecordsIngested: int | None = None
