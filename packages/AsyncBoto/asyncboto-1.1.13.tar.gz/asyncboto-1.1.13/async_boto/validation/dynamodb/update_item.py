from typing import Literal

from pydantic import BaseModel, constr

from .data_types.attribute_value import AttributeValue, AttributeValueDict
from .data_types.attribute_value_update import AttributeValueUpdate
from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel
from .data_types.expected_attribute_value import ExpectedAttributeValue
from .data_types.item_collection_metrics import (
    ItemCollectionMetrics as ItemCollectionMetricsModel,
)


class UpdateItemRequest(BaseModel):
    """
    Request model for the UpdateItem operation.

    Attributes
    ----------
    Key : Dict[str, AttributeValue]
        The primary key of the item to be updated.
    TableName : constr(min_length=1, max_length=1024)
        The name of the table containing the item to update.
    AttributeUpdates : Optional[Dict[str, AttributeValueUpdate]]
        Legacy parameter for attribute updates.
    ConditionalOperator : Optional[Literal["AND", "OR"]]
        Legacy parameter for conditional operator.
    ConditionExpression : Optional[str]
        A condition that must be satisfied for a conditional update to succeed.
    Expected : Optional[Dict[str, ExpectedAttributeValue]]
        Legacy parameter for expected attribute values.
    ExpressionAttributeNames : Optional[Dict[str, str]]
        Substitution tokens for attribute names in an expression.
    ExpressionAttributeValues : Optional[Dict[str, AttributeValue]]
        Values that can be substituted in an expression.
    ReturnConsumedCapacity : Optional[Literal["INDEXES", "TOTAL", "NONE"]]
        Level of detail about throughput consumption to be returned.
    ReturnItemCollectionMetrics : Optional[Literal["SIZE", "NONE"]]
        Whether item collection metrics are returned.
    ReturnValues : Optional[Literal["NONE", "ALL_OLD", "UPDATED_OLD", "ALL_NEW",
    "UPDATED_NEW"]]
        The item attributes to return as they appear before or after the update.
    ReturnValuesOnConditionCheckFailure : Optional[Literal["ALL_OLD", "NONE"]]
        The item attributes to return if the update fails a condition check.
    UpdateExpression : Optional[str]
        An expression that defines one or more attributes to be updated.
    """

    Key: AttributeValueDict
    TableName: constr(min_length=1, max_length=1024)
    AttributeUpdates: dict[str, AttributeValueUpdate] | None = None
    ConditionalOperator: Literal["AND", "OR"] | None = None
    ConditionExpression: str | None = None
    Expected: dict[str, ExpectedAttributeValue] | None = None
    ExpressionAttributeNames: dict[str, str] | None = None
    ExpressionAttributeValues: dict[str, AttributeValue] | None = None
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None
    ReturnItemCollectionMetrics: Literal["SIZE", "NONE"] | None = None
    ReturnValues: (
        Literal["NONE", "ALL_OLD", "UPDATED_OLD", "ALL_NEW", "UPDATED_NEW"] | None
    ) = None  # noqa: E501
    ReturnValuesOnConditionCheckFailure: Literal["ALL_OLD", "NONE"] | None = None
    UpdateExpression: str | None = None


class UpdateItemResponse(BaseModel):
    """
    Response model for the UpdateItem operation.

    Attributes
    ----------
    Attributes : Optional[Dict[str, AttributeValue]]
        A map of attribute values as they appear before or after the UpdateItem
        operation.
    ConsumedCapacity : Optional[ConsumedCapacity]
        The capacity units consumed by the UpdateItem operation.
    ItemCollectionMetrics : Optional[ItemCollectionMetrics]
        Information about item collections affected by the UpdateItem operation.
    """

    Attributes: dict[str, AttributeValue] | None = None
    ConsumedCapacity: ConsumedCapacityModel | None = None
    ItemCollectionMetrics: ItemCollectionMetricsModel | None = None
