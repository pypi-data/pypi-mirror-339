# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel

from .attribute_value import AttributeValue


class Condition(BaseModel):
    """
    Represents the selection criteria for a Query or Scan operation.

    Attributes
    ----------
    ComparisonOperator : Literal["EQ", "NE", "IN", "LE", "LT", "GE", "GT", "BETWEEN", "NOT_NULL", "NULL", "CONTAINS", "NOT_CONTAINS", "BEGINS_WITH"]
        A comparator for evaluating attributes. For example, equals, greater than, less than, etc.
        Valid Values: EQ, NE, IN, LE, LT, GE, GT, BETWEEN, NOT_NULL, NULL, CONTAINS, NOT_CONTAINS, BEGINS_WITH.
        - EQ: Equal. Supported for all data types, including lists and maps.
        - NE: Not equal. Supported for all data types, including lists and maps.
        - IN: Checks for matching elements in a list.
        - LE: Less than or equal. Supported for String, Number, or Binary (not a set type).
        - LT: Less than. Supported for String, Number, or Binary (not a set type).
        - GE: Greater than or equal. Supported for String, Number, or Binary (not a set type).
        - GT: Greater than. Supported for String, Number, or Binary (not a set type).
        - BETWEEN: Greater than or equal to the first value, and less than or equal to the second value.
        - NOT_NULL: The attribute exists. Supported for all data types, including lists and maps.
        - NULL: The attribute does not exist. Supported for all data types, including lists and maps.
        - CONTAINS: Checks for a subsequence, or value in a set.
        - NOT_CONTAINS: Checks for absence of a subsequence, or absence of a value in a set.
        - BEGINS_WITH: Checks for a prefix. Supported for String or Binary
        (not a Number or a set type).
    AttributeValueList : Optional[List[AttributeValue]]
        One or more values to evaluate against the supplied attribute. The number of
        values in the list depends on the ComparisonOperator being used.
    """

    ComparisonOperator: Literal[
        "EQ",
        "NE",
        "IN",
        "LE",
        "LT",
        "GE",
        "GT",
        "BETWEEN",
        "NOT_NULL",
        "NULL",
        "CONTAINS",
        "NOT_CONTAINS",
        "BEGINS_WITH",
    ]
    AttributeValueList: list[AttributeValue] | None = None
