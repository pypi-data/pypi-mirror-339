from typing import Literal

from pydantic import BaseModel, Field

from .data_types.attribute_value import AttributeValueDict
from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel
from .data_types.expected_attribute_value import ExpectedAttributeValue
from .data_types.item_collection_metrics import (
    ItemCollectionMetrics as ItemCollectionMetricsModel,
)


class DeleteItemRequest(BaseModel):
    TableName: str = Field(..., min_length=1, max_length=1024)
    Key: AttributeValueDict
    ConditionalOperator: Literal["AND", "OR"] | None = None
    ConditionExpression: str | None = None
    Expected: dict[str, ExpectedAttributeValue] | None = None
    ExpressionAttributeNames: dict[str, str] | None = None
    ExpressionAttributeValues: AttributeValueDict | None = None
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None
    ReturnItemCollectionMetrics: Literal["SIZE", "NONE"] | None = None
    ReturnValues: Literal["NONE", "ALL_OLD"] | None = None
    ReturnValuesOnConditionCheckFailure: Literal["ALL_OLD", "NONE"] | None = None

    @classmethod
    def from_python_dict(cls, data: dict, **kwargs):
        return cls(Key=AttributeValueDict.from_python_dict(data), **kwargs)


class DeleteItemResponse(BaseModel):
    Attributes: AttributeValueDict | None = None
    ConsumedCapacity: ConsumedCapacityModel | None = None
    ItemCollectionMetrics: ItemCollectionMetricsModel | None = None
