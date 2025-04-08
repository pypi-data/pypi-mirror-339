from pydantic import BaseModel, constr

from .multi_measure_attribute_mapping import MultiMeasureAttributeMapping


class MultiMeasureMappings(BaseModel):
    """
    Represents the mappings of multi-measure attributes.

    Attributes
    ----------
    MultiMeasureAttributeMappings : List[MultiMeasureAttributeMapping]
        The list of multi-measure attribute mappings.
    TargetMultiMeasureName : str | None
        The target multi-measure name.
    """

    MultiMeasureAttributeMappings: list[MultiMeasureAttributeMapping]
    TargetMultiMeasureName: constr(min_length=1) | None = None
