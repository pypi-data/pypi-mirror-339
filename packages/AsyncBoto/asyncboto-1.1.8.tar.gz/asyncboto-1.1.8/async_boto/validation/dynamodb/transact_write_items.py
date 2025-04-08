from typing import Literal

from pydantic import BaseModel, constr

from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel
from .data_types.item_collection_metrics import (
    ItemCollectionMetrics as ItemCollectionMetricsModel,
)
from .data_types.transact_write_item import TransactWriteItem


class TransactWriteItemsRequest(BaseModel):
    TransactItems: list[TransactWriteItem]
    ClientRequestToken: constr(min_length=1, max_length=36) | None = None
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None
    ReturnItemCollectionMetrics: Literal["SIZE", "NONE"] | None = None


class TransactWriteItemsResponse(BaseModel):
    """
    Response model for the TransactWriteItems operation.

    Attributes
    ----------
    ConsumedCapacity : Optional[List[ConsumedCapacity]]
        An array of ConsumedCapacity objects.
    ItemCollectionMetrics : Optional[Dict[str, List[ItemCollectionMetrics]]]
        A map of table names to arrays of ItemCollectionMetrics objects.
    """

    ConsumedCapacity: list[ConsumedCapacityModel] | None = None
    ItemCollectionMetrics: dict[str, list[ItemCollectionMetricsModel]] | None = None
