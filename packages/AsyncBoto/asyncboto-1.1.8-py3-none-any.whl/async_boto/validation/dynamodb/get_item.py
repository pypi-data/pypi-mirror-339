from typing import Literal

from pydantic import BaseModel, Field

from .data_types.attribute_value import AttributeValueDict
from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel


class GetItemRequest(BaseModel):
    Key: AttributeValueDict
    TableName: str = Field(..., min_length=1, max_length=1024)
    AttributesToGet: list[str] | None = None
    ConsistentRead: bool | None = None
    ExpressionAttributeNames: dict[str, str] | None = None
    ProjectionExpression: str | None = None
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None


class GetItemResponse(BaseModel):
    ConsumedCapacity: ConsumedCapacityModel | None = None
    Item: AttributeValueDict | None = None
