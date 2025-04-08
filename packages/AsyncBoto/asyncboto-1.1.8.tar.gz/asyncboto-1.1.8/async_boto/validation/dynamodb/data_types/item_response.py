from pydantic import BaseModel

from .attribute_value import AttributeValueDict


class ItemResponse(BaseModel):
    """
    Details for the requested item.

    Attributes
    ----------
    Item : Optional[AttributeValueDict]
        Map of attribute data consisting of the data type and attribute value.
    """

    Item: AttributeValueDict | None = None
