from typing import Literal

from pydantic import BaseModel

from .data_types.attribute_value import AttributeValueDict
from .data_types.consumed_capacity import ConsumedCapacity
from .data_types.keys_and_attributes import KeysAndAttributes


class BatchGetItemRequest(BaseModel):
    RequestItems: dict[str, KeysAndAttributes]
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None


class BatchGetItemResponse(BaseModel):
    ConsumedCapacity: list[ConsumedCapacity] | None = None
    Responses: dict[str, list[AttributeValueDict]] | None = None
    UnprocessedKeys: dict[str, KeysAndAttributes] | None = None
