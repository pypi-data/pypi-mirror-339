from typing import Literal

from pydantic import BaseModel

from .data_types.consumed_capacity import ConsumedCapacity
from .data_types.item_collection_metrics import ItemCollectionMetrics
from .data_types.write_request import WriteRequest


class BatchWriteItemRequest(BaseModel):
    RequestItems: dict[str, list[WriteRequest]]
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] = "NONE"
    ReturnItemCollectionMetrics: Literal["SIZE", "NONE"] = "NONE"


class BatchWriteItemsResponse(BaseModel):
    UnprocessedItems: dict[str, list[WriteRequest]]
    ItemCollectionMetrics: dict[str, list[ItemCollectionMetrics]] | None = None
    ConsumedCapacity: list[ConsumedCapacity] | None = None
