from typing import Literal

from pydantic import BaseModel, Field, constr

from .attribute_value import AttributeValueDict


class Put(BaseModel):
    """
    Represents a request to perform a PutItem operation.

    Attributes
    ----------
    Item : Dict[str, AttributeValue]
        A map of attribute name to attribute values, representing the primary key of
        the item to be written by PutItem.
    TableName : str
        Name of the table in which to write the item.
    ConditionExpression : Optional[str]
        A condition that must be satisfied in order for a conditional update to succeed.
    ExpressionAttributeNames : Optional[Dict[str, str]]
        One or more substitution tokens for attribute names in an expression.
    ExpressionAttributeValues : Optional[Dict[str, AttributeValue]]
        One or more values that can be substituted in an expression.
    ReturnValuesOnConditionCheckFailure : Optional[Literal['ALL_OLD', 'NONE']]
        Use ReturnValuesOnConditionCheckFailure to get the item attributes if the
        Put condition fails.
    """

    Item: AttributeValueDict = Field(..., max_length=65535)
    TableName: constr(min_length=1, max_length=1024)
    ConditionExpression: str | None = None
    ExpressionAttributeNames: dict[str, str] | None = None
    ExpressionAttributeValues: AttributeValueDict | None = None
    ReturnValuesOnConditionCheckFailure: Literal["ALL_OLD", "NONE"] | None = None
