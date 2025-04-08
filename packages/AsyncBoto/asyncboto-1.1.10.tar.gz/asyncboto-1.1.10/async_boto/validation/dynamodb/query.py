from typing import Literal

from pydantic import BaseModel, Field

from .data_types.attribute_value import AttributeValueDict
from .data_types.condition import Condition
from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel


class QueryRequest(BaseModel):
    TableName: str = Field(..., min_length=1, max_length=1024)
    AttributesToGet: list[str] | None = None
    ConditionalOperator: Literal["AND", "OR"] | None = None
    ConsistentRead: bool | None = None
    ExclusiveStartKey: AttributeValueDict | None = None
    ExpressionAttributeNames: dict[str, str] | None = None
    ExpressionAttributeValues: AttributeValueDict | None = None
    FilterExpression: str | None = None
    IndexName: str | None = Field(None, min_length=3, max_length=255)
    KeyConditionExpression: str | None = None
    KeyConditions: dict[str, Condition] | None = None
    Limit: int | None = Field(None, ge=1)
    ProjectionExpression: str | None = None
    QueryFilter: dict[str, Condition] | None = None
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None
    ScanIndexForward: bool | None = None
    Select: (
        Literal[
            "ALL_ATTRIBUTES", "ALL_PROJECTED_ATTRIBUTES", "SPECIFIC_ATTRIBUTES", "COUNT"
        ]
        | None
    ) = None  # noqa: E501


class QueryResponse(BaseModel):
    ConsumedCapacity: ConsumedCapacityModel | None = None
    Count: int | None = None
    Items: list[AttributeValueDict] | None = None
    LastEvaluatedKey: AttributeValueDict | None = None
    ScannedCount: int | None = None
