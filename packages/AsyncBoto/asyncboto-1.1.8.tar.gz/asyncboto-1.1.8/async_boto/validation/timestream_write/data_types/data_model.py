# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, Field, constr

from .dimension_mapping import DimensionMapping
from .mixed_measure_mapping import MixedMeasureMapping
from .multi_measure_mappings import MultiMeasureMappings as MultiMeasureMappingsModel


class DataModel(BaseModel):
    """
    Data model for a batch load task.

    Attributes
    ----------
    DimensionMappings : List[DimensionMapping]
        Source to target mappings for dimensions.
    MeasureNameColumn : str | None
        Measure name column.
    MixedMeasureMappings : List[MixedMeasureMapping] | None
        Source to target mappings for measures.
    MultiMeasureMappings : MultiMeasureMappings | None
        Source to target mappings for multi-measure records.
    TimeColumn : str | None
        Source column to be mapped to time.
    TimeUnit : Literal["MILLISECONDS", "SECONDS", "MICROSECONDS", "NANOSECONDS"] | None
        The granularity of the timestamp unit.
    """

    DimensionMappings: list[DimensionMapping] = Field(..., min_length=1)
    MeasureNameColumn: constr(min_length=1, max_length=256) | None = None
    MixedMeasureMappings: list[MixedMeasureMapping] | None = Field(
        default=None, min_length=1
    )
    MultiMeasureMappings: MultiMeasureMappingsModel | None = None
    TimeColumn: constr(min_length=1, max_length=256) | None = None
    TimeUnit: (
        Literal["MILLISECONDS", "SECONDS", "MICROSECONDS", "NANOSECONDS"] | None
    ) = None
