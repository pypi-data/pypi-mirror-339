from typing import Literal

from pydantic import BaseModel

from .multi_measure_attribute_mapping import MultiMeasureAttributeMapping


class MixedMeasureMapping(BaseModel):
    """
    MixedMeasureMappings are mappings that can be used to ingest data into a mixture
    of narrow and multi measures in the derived table.

    Parameters
    ----------
    MeasureValueType : str
        Type of the value that is to be read from sourceColumn. If the mapping is
        for MULTI,
        use MeasureValueType.MULTI.
    MeasureName : Optional[str]
        Refers to the value of measure_name in a result row. This field is required if
        MeasureNameColumn is provided.
    MultiMeasureAttributeMappings : Optional[List[MultiMeasureAttributeMapping]]
        Required when measureValueType is MULTI. Attribute mappings for MULTI value
        measures.
    SourceColumn : Optional[str]
        This field refers to the source column from which measure-value is to be read
        for result materialization.
    TargetMeasureName : Optional[str]
        Target measure name to be used. If not provided, the target measure name
        by default
        would be measure-name if provided, or sourceColumn otherwise.
    """

    MeasureValueType: Literal["BIGINT", "BOOLEAN", "DOUBLE", "VARCHAR", "MULTI"]
    MeasureName: str | None = None
    MultiMeasureAttributeMappings: list[MultiMeasureAttributeMapping] | None = None
    SourceColumn: str | None = None
    TargetMeasureName: str | None = None
