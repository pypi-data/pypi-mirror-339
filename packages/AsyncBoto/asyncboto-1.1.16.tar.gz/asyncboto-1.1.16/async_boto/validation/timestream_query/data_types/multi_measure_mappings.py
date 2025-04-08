from pydantic import BaseModel

from .multi_measure_attribute_mapping import MultiMeasureAttributeMapping


class MultiMeasureMappings(BaseModel):
    """
    MultiMeasureMappings can be used to ingest data as multi measures in
    the derived table.
    Only one of MixedMeasureMappings or MultiMeasureMappings is to be provided.

    Parameters
    ----------
    MultiMeasureAttributeMappings : List[MultiMeasureAttributeMapping]
        Required. Attribute mappings to be used for mapping query results to ingest data
        for multi-measure attributes.
    TargetMultiMeasureName : Optional[str]
        The name of the target multi-measure name in the derived table.
        This input is required
        when measureNameColumn is not provided. If MeasureNameColumn is provided,
        then value from that column will be used as multi-measure name.
    """

    MultiMeasureAttributeMappings: list[MultiMeasureAttributeMapping]
    TargetMultiMeasureName: str | None = None
