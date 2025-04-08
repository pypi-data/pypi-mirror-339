from typing import Literal

from pydantic import BaseModel, constr

from .attribute_value import AttributeValueDict


class Delete(BaseModel):
    """
    Represents a request to perform a DeleteItem operation.

    Attributes
    ----------
    Key : AttributeValueDict
        The primary key of the item to be deleted. Each element consists of an attribute
         name and a value for that attribute.
    TableName : constr(min_length=1, max_length=1024)
        Name of the table in which the item to be deleted resides. You can also provide
        the Amazon Resource Name (ARN) of the table in this parameter.
    ConditionExpression : Optional[str]
        A condition that must be satisfied in order for a conditional delete to succeed.
    ExpressionAttributeNames : Optional[Dict[str, str]]
        One or more substitution tokens for attribute names in an expression.
    ExpressionAttributeValues : Optional[AttributeValueDict]
        One or more values that can be substituted in an expression.
    ReturnValuesOnConditionCheckFailure : Optional[Literal["ALL_OLD", "NONE"]]
        Use ReturnValuesOnConditionCheckFailure to get the item attributes if the
        Delete condition fails.
    """

    Key: AttributeValueDict
    TableName: constr(min_length=1, max_length=1024)
    ConditionExpression: str | None = None
    ExpressionAttributeNames: dict[str, str] | None = None
    ExpressionAttributeValues: AttributeValueDict | None = None
    ReturnValuesOnConditionCheckFailure: Literal["ALL_OLD", "NONE"] | None = None
