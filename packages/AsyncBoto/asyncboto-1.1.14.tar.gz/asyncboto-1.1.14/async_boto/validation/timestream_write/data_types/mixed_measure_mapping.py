# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr

from .multi_measure_attribute_mapping import MultiMeasureAttributeMapping


class MixedMeasureMapping(BaseModel):
    """
    Represents the mapping of mixed measure values.

    Attributes
    ----------
    MeasureValueType : str
        The type of the measure value.
    MeasureName : str | None
        The name of the measure.
    MultiMeasureAttributeMappings : List[MultiMeasureAttributeMapping] | None
        The list of multi-measure attribute mappings.
    SourceColumn : str | None
        The source column of the measure.
    TargetMeasureName : str | None
        The target measure name.
    """

    MeasureValueType: Literal[
        "DOUBLE", "BIGINT", "VARCHAR", "BOOLEAN", "TIMESTAMP", "MULTI"
    ]
    MeasureName: constr(min_length=1) | None = None
    MultiMeasureAttributeMappings: list[MultiMeasureAttributeMapping] | None = None
    SourceColumn: constr(min_length=1) | None = None
    TargetMeasureName: constr(min_length=1) | None = None
