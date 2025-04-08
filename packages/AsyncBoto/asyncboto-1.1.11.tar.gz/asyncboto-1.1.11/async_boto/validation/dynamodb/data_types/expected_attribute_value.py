# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel

from .attribute_value import AttributeValue


class ExpectedAttributeValue(BaseModel):
    """
    Represents a condition to be compared with an attribute value. This condition can be
    used with DeleteItem, PutItem, or UpdateItem operations; if the comparison evaluates
    to true, the operation succeeds; if not, the operation fails.

    Attributes
    ----------
    AttributeValueList : Optional[List[AttributeValue]]
        One or more values to evaluate against the supplied attribute.
        The number of values in the list depends on the ComparisonOperator being used.
    ComparisonOperator : Optional[Literal["EQ", "NE", "LE", "LT", "GE", "GT", "NOT_NULL", "NULL", "CONTAINS", "NOT_CONTAINS", "BEGINS_WITH", "IN", "BETWEEN"]]
        A comparator for evaluating attributes in the AttributeValueList.
        Valid values are EQ, NE, LE, LT, GE, GT, NOT_NULL, NULL, CONTAINS,
        NOT_CONTAINS, BEGINS_WITH, IN, BETWEEN.
        - EQ: Equal. Supported for all data types, including lists and maps.
        - NE: Not equal. Supported for all data types, including lists and maps.
        - LE: Less than or equal. Supported for String, Number, or Binary (not a set type).
        - LT: Less than. Supported for String, Number, or Binary (not a set type).
        - GE: Greater than or equal. Supported for String, Number, or Binary (not a set type).
        - GT: Greater than. Supported for String, Number, or Binary (not a set type).
        - NOT_NULL: The attribute exists. Supported for all data types, including lists and maps.
        - NULL: The attribute does not exist. Supported for all data types, including lists and maps.
        - CONTAINS: Checks for a subsequence, or value in a set. Supported for String, Number, or Binary (not a set type).
        - NOT_CONTAINS: Checks for absence of a subsequence, or absence of a value in a set. Supported for String, Number, or Binary (not a set type).
        - BEGINS_WITH: Checks for a prefix. Supported for String or Binary (not a Number or a set type).
        - IN: Checks for matching elements in a list. Supported for String, Number, or Binary.
        - BETWEEN: Greater than or equal to the first value, and less than or equal to the second value. Supported for String, Number, or Binary (not a set type).
    Exists : Optional[bool]
        Causes DynamoDB to evaluate the value before attempting a conditional operation.
    Value : Optional[AttributeValue]
        Represents the data for the expected attribute.
    """

    AttributeValueList: list[AttributeValue] | None = None
    ComparisonOperator: (
        Literal[
            "EQ",
            "NE",
            "LE",
            "LT",
            "GE",
            "GT",
            "NOT_NULL",
            "NULL",
            "CONTAINS",
            "NOT_CONTAINS",
            "BEGINS_WITH",
            "IN",
            "BETWEEN",
        ]
        | None
    ) = None
    Exists: bool | None = None
    Value: AttributeValue | None = None
