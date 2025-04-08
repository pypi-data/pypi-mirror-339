from typing import Literal

from pydantic import BaseModel, Field

from .data_types.attribute_value import AttributeValueDict
from .data_types.condition import Condition
from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel


class ScanRequest(BaseModel):
    TableName: str = Field(..., min_length=1, max_length=1024)
    AttributesToGet: list[str] | None = Field(None, max_length=65535)
    ConditionalOperator: Literal["AND", "OR"] | None = None
    ConsistentRead: bool | None = None
    ExclusiveStartKey: AttributeValueDict | None = None
    ExpressionAttributeNames: dict[str, str] | None = None
    ExpressionAttributeValues: AttributeValueDict | None = None
    FilterExpression: str | None = None
    IndexName: str | None = Field(None, min_length=3, max_length=255)
    Limit: int | None = Field(None, ge=1)
    ProjectionExpression: str | None = None
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None
    ScanFilter: dict[str, Condition] | None = None
    Segment: int | None = Field(None, ge=0, le=999999)
    Select: (
        Literal[
            "ALL_ATTRIBUTES", "ALL_PROJECTED_ATTRIBUTES", "SPECIFIC_ATTRIBUTES", "COUNT"
        ]
        | None
    ) = None  # noqa: E501
    TotalSegments: int | None = Field(None, ge=1, le=1000000)


class ScanResponse(BaseModel):
    ConsumedCapacity: ConsumedCapacityModel | None = None
    Count: int | None = None
    Items: list[AttributeValueDict] | None = None
    LastEvaluatedKey: AttributeValueDict | None = None
    ScannedCount: int | None = None
