from typing import Literal

from pydantic import BaseModel, constr

from .attribute_value import AttributeValueDict


class ConditionCheck(BaseModel):
    """
    Represents a request to perform a check that an item exists or to check the
    condition of specific attributes of the item.

    Attributes
    ----------
    ConditionExpression : str
        A condition that must be satisfied in order for a conditional update to succeed.
    Key : AttributeValueDict
        The primary key of the item to be checked. Each element consists of an attribute
         name and a value for that attribute. Maximum length of 65535.
    TableName : constr(min_length=1, max_length=1024)
        Name of the table for the check item request. You can also provide the Amazon
        Resource Name (ARN) of the table in this parameter.
    ExpressionAttributeNames : Optional[Dict[str, str]]
        One or more substitution tokens for attribute names in an expression. Maximum
        length of 65535.
    ExpressionAttributeValues : Optional[AttributeValueDict]
        One or more values that can be substituted in an expression.
    ReturnValuesOnConditionCheckFailure : Optional[Literal["ALL_OLD", "NONE"]]
        Use ReturnValuesOnConditionCheckFailure to get the item attributes if the
        ConditionCheck condition fails. Valid values are: NONE and ALL_OLD.
    """

    ConditionExpression: str
    Key: AttributeValueDict
    TableName: constr(min_length=1, max_length=1024)
    ExpressionAttributeNames: dict[str, str] | None = None
    ExpressionAttributeValues: AttributeValueDict | None = None
    ReturnValuesOnConditionCheckFailure: Literal["ALL_OLD", "NONE"] | None = None
