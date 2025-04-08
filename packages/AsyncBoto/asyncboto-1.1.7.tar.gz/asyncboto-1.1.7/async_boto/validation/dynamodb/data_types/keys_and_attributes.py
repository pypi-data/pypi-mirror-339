from pydantic import BaseModel, conlist

from .attribute_value import AttributeValueDict


class KeysAndAttributes(BaseModel):
    """
    Represents a set of primary keys and, for each key, the attributes to retrieve
    from the table.

    Attributes
    ----------
    Keys : conlist(AttributeValueDict, min_items=1, max_items=100)
        The primary key attribute values that define the items and the attributes
        associated with the items.
    AttributesToGet : Optional[List[str]]
        This is a legacy parameter. Use ProjectionExpression instead.
    ConsistentRead : Optional[bool]
        The consistency of a read operation.
    ExpressionAttributeNames : Optional[Dict[str, str]]
        One or more substitution tokens for attribute names in an expression.
    ProjectionExpression : Optional[str]
        A string that identifies one or more attributes to retrieve from the table.
    """

    Keys: conlist(AttributeValueDict, min_length=1, max_length=100)
    AttributesToGet: list[str] | None = None
    ConsistentRead: bool | None = None
    ExpressionAttributeNames: dict[str, str] | None = None
    ProjectionExpression: str | None = None
