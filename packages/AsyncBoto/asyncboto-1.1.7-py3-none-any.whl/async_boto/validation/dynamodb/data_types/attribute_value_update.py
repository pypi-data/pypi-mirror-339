from typing import Literal

from pydantic import BaseModel

from .attribute_value import AttributeValue


class AttributeValueUpdate(BaseModel):
    Action: Literal["ADD", "PUT", "DELETE"] | None = None
    Value: AttributeValue | None = None
