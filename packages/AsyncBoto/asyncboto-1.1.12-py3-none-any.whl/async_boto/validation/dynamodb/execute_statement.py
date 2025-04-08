from typing import Literal

from pydantic import BaseModel, conint, constr

from .data_types.attribute_value import AttributeValue, AttributeValueDict
from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel


class ExecuteStatementRequest(BaseModel):
    """
    Allows you to perform reads and singleton writes on data stored in DynamoDB,
    using PartiQL.

    Attributes
    ----------
    Statement : str
        The PartiQL statement representing the operation to run.
    ConsistentRead : Optional[bool]
        Determines the read consistency model: If set to true, then the operation uses
        strongly consistent reads; otherwise, the operation uses eventually consistent
        reads.
    Limit : Optional[int]
        The maximum number of items to evaluate (not necessarily the number of matching
        items).
    NextToken : Optional[str]
        An optional string that, if supplied, must be copied from the output of a
        previous call to the same operation.
    Parameters : Optional[List[AttributeValue]]
        The parameters for the PartiQL statement.
    ReturnConsumedCapacity : Optional[Literal['INDEXES', 'TOTAL', 'NONE']]
        Determines the level of detail about either provisioned or on-demand throughput
        consumption that is returned in the response.
    ReturnValuesOnConditionCheckFailure : Optional[Literal['ALL_OLD', 'NONE']]
        An optional parameter that returns the item attributes for a condition check
        failure.
    """

    Statement: constr(min_length=1, max_length=8192)
    ConsistentRead: bool | None = None
    Limit: conint(ge=1) | None = None
    NextToken: constr(min_length=1, max_length=32768) | None = None
    Parameters: list[AttributeValue] | None = None
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None
    ReturnValuesOnConditionCheckFailure: Literal["ALL_OLD", "NONE"] | None = None


class ExecuteStatementResponse(BaseModel):
    """
    Response for the ExecuteStatement operation.

    Attributes
    ----------
    ConsumedCapacity : Optional[ConsumedCapacity]
        The capacity units consumed by an operation.
    Items : Optional[List[Dict[str, AttributeValue]]]
        The items returned by the operation.
    LastEvaluatedKey : Optional[Dict[str, AttributeValue]]
        The primary key of the item where the operation stopped, inclusive of the
        previous result set.
    NextToken : Optional[str]
        An optional string that, if supplied, must be copied from the output of a
        previous call to the same operation.
    """

    ConsumedCapacity: ConsumedCapacityModel | None = None
    Items: list[AttributeValueDict] | None = None
    LastEvaluatedKey: AttributeValueDict | None = None
    NextToken: constr(min_length=1, max_length=32768) | None = None
