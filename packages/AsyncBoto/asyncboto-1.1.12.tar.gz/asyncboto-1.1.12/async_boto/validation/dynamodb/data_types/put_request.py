from pydantic import BaseModel

from .attribute_value import AttributeValueDict


class PutRequest(BaseModel):
    """
    Represents a request to perform a PutItem operation on an item.

    Attributes
    ----------
    Item : Dict[str, AttributeValue]
        A map of attribute name to attribute values, representing the primary key of
        an item to be processed by PutItem.
    """

    Item: AttributeValueDict

    @classmethod
    def from_python_dict(cls, data: dict):
        return cls(Item=AttributeValueDict.from_python_dict(data))
