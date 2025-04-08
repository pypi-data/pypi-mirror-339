from typing import Literal

from pydantic import BaseModel, Field

from .attribute_value import AttributeValue


class BatchStatementRequest(BaseModel):
    """
    A PartiQL batch statement request.

    Attributes
    ----------
    Statement : str
        A valid PartiQL statement. Minimum length of 1. Maximum length of 8192.
    ConsistentRead : Optional[bool]
        The read consistency of the PartiQL batch request.
    Parameters : Optional[List[AttributeValue]]
        The parameters associated with a PartiQL statement in the batch request.
        Minimum number of 1 item.
    ReturnValuesOnConditionCheckFailure : Optional[Literal['ALL_OLD', 'NONE']]
        An optional parameter that returns the item attributes for a PartiQL batch
        request operation that failed a condition check.
    """

    Statement: str = Field(..., min_length=1, max_length=8192)
    ConsistentRead: bool | None = None
    Parameters: list[AttributeValue] | None = Field(None, min_length=1)
    ReturnValuesOnConditionCheckFailure: Literal["ALL_OLD", "NONE"] | None = None
