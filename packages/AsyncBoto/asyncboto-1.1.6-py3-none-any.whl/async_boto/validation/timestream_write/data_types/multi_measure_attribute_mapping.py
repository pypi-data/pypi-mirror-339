# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, constr


class MultiMeasureAttributeMapping(BaseModel):
    """
    Represents the mapping of multi-measure attributes.

    Attributes
    ----------
    SourceColumn : str
        The source column of the measure.
    MeasureValueType : str | None
        The type of the measure value.
    TargetMultiMeasureAttributeName : str | None
        The target multi-measure attribute name.
    """

    SourceColumn: constr(min_length=1)
    MeasureValueType: (
        Literal["DOUBLE", "BIGINT", "BOOLEAN", "VARCHAR", "TIMESTAMP"] | None
    ) = None
    TargetMultiMeasureAttributeName: constr(min_length=1) | None = None
