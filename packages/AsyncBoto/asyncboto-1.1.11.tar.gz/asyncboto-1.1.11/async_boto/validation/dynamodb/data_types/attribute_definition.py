from typing import Literal

from pydantic import BaseModel, Field


class AttributeDefinition(BaseModel):
    AttributeName: str = Field(..., min_length=1, max_length=255)
    AttributeType: Literal["S", "N", "B"]
