from pydantic import BaseModel, Field

from .dimension_mapping import DimensionMapping
from .mixed_measure_mapping import MixedMeasureMapping
from .multi_measure_mappings import MultiMeasureMappings


class TimestreamConfiguration(BaseModel):
    """
    Configuration to write data into Timestream database and table. This
    configuration allows the user to map the query result select columns
    into the destination table columns.

    Parameters
    ----------
    DatabaseName : str
        Name of Timestream database to which the query result will be written.
    DimensionMappings : List[DimensionMapping]
        This is to allow mapping column(s) from the query result to the
        dimension in the destination table.
    TableName : str
        Name of Timestream table that the query result will be written to.
        The table should be within the same database that is provided in
        Timestream configuration.
    TimeColumn : str
        Column from query result that should be used as the time column in
        destination table. Column type for this should be TIMESTAMP.
    MeasureNameColumn : Optional[str], optional
        Name of the measure column.
    MixedMeasureMappings : Optional[List[MixedMeasureMapping]], optional
        Specifies how to map measures to multi-measure records.
    MultiMeasureMappings : Optional[MultiMeasureMappings], optional
        Multi-measure mappings.
    """

    DatabaseName: str
    DimensionMappings: list[DimensionMapping]
    TableName: str
    TimeColumn: str
    MeasureNameColumn: str | None = None
    MixedMeasureMappings: list[MixedMeasureMapping] | None = Field(None, min_length=1)
    MultiMeasureMappings: MultiMeasureMappings | None = None
