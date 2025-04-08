from pydantic import BaseModel, constr

from .attribute_value import AttributeValueDict


class Get(BaseModel):
    """
    Specifies an item and related attribute values to retrieve in a TransactGetItem
    object.

    Attributes
    ----------
    Key : AttributeValueDict
        A map of attribute names to AttributeValue objects that specifies the primary
        key of the item to retrieve.
    TableName : constr(min_length=1, max_length=1024)
        The name of the table from which to retrieve the specified item.
    ExpressionAttributeNames : Optional[Dict[str, str]]
        One or more substitution tokens for attribute names in the ProjectionExpression
        parameter.
    ProjectionExpression : Optional[str]
        A string that identifies one or more attributes of the specified item to
        retrieve from the table.
    """

    Key: AttributeValueDict
    TableName: constr(min_length=1, max_length=1024)
    ExpressionAttributeNames: dict[str, str] | None = None
    ProjectionExpression: str | None = None
