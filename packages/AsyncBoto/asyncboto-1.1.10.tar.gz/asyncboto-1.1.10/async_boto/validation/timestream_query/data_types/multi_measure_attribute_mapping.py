from typing import Literal

from pydantic import BaseModel


class MultiMeasureAttributeMapping(BaseModel):
    """
    Attribute mapping for MULTI value measures.

    Parameters
    ----------
    MeasureValueType : str
        Type of the attribute to be read from the source column.
    SourceColumn : str
        Source column from where the attribute value is to be read.
    TargetMultiMeasureAttributeName : Optional[str]
        Custom name to be used for attribute name in derived table.
        If not provided, source column name would be used.
    """

    MeasureValueType: Literal["BIGINT", "BOOLEAN", "DOUBLE", "VARCHAR", "TIMESTAMP"]
    SourceColumn: str
    TargetMultiMeasureAttributeName: str | None = None
