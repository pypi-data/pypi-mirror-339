from typing import Literal

from pydantic import BaseModel

from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel
from .data_types.item_response import ItemResponse
from .data_types.transact_get_item import TransactGetItem


class TransactGetItemsRequest(BaseModel):
    """
    Request model for the TransactGetItems operation.

    Attributes
    ----------
    TransactItems : List[TransactGetItem]
        An ordered array of up to 100 TransactGetItem objects.
    ReturnConsumedCapacity : Optional[str]
        Consumed capacity information to be returned.
    """

    TransactItems: list[TransactGetItem]
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None


class TransactGetItemsResponse(BaseModel):
    """
    Response model for the TransactGetItems operation.

    Attributes
    ----------
    ConsumedCapacity : Optional[List[ConsumedCapacity]]
        An array of ConsumedCapacity objects.
    Responses : List[Optional[ItemResponse]]
        An ordered array of up to 100 ItemResponse objects.
    """

    ConsumedCapacity: list[ConsumedCapacityModel] | None = None
    Responses: list[ItemResponse | None]
