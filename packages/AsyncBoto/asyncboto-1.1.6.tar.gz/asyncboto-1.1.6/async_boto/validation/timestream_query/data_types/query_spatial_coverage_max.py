from pydantic import BaseModel, Field


class QuerySpatialCoverageMax(BaseModel):
    """
    Provides insights into the table with the most sub-optimal spatial range
    scanned by your query.

    Parameters
    ----------
    PartitionKey : Optional[List[str]], optional
        The partition key used for partitioning, which can be a default
        `measure_name` or a customer defined partition key.
    TableArn : Optional[str], optional
        The Amazon Resource Name (ARN) of the table with the most sub-optimal
        spatial pruning.
    Value : Optional[float], optional
        The maximum ratio of spatial coverage.
    """

    PartitionKey: list[str] | None = None
    TableArn: str | None = Field(None, min_length=1, max_length=2048)
    Value: float | None = None
