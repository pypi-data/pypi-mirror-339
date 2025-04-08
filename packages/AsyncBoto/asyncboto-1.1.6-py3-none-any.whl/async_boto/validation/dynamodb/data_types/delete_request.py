from pydantic import BaseModel

from .attribute_value import AttributeValueDict


class DeleteRequest(BaseModel):
    """
    Represents a request to perform a DeleteItem operation on an item.

    Attributes
    ----------
    Key : AttributeValueDict
        A map of attribute name to attribute values, representing the
        primary key of the item to delete. All of the table's primary key
        attributes must be specified, and their data types must match those of
        the table's key schema.
    """

    Key: AttributeValueDict

    @classmethod
    def from_python_dict(cls, data: dict):
        return cls(Key=AttributeValueDict.from_python_dict(data))
