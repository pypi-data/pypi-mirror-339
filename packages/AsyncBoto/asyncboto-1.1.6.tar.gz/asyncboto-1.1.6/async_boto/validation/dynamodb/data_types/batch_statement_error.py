from pydantic import BaseModel

from .attribute_value import AttributeValueDict


class BatchStatementError(BaseModel):
    """
    An error associated with a statement in a PartiQL batch that was run.

    Attributes
    ----------
    Code : Optional[str]
        The error code associated with the failed PartiQL batch statement.
        Valid Values: ConditionalCheckFailed, ItemCollectionSizeLimitExceeded,
        RequestLimitExceeded, ValidationError, ProvisionedThroughputExceeded,
        TransactionConflict, ThrottlingError, InternalServerError, ResourceNotFound,
        AccessDenied, DuplicateItem.
    Item : Optional[AttributeValueDict]
        The item which caused the condition check to fail. This will be set if
        ReturnValuesOnConditionCheckFailure is specified as ALL_OLD.
        Maximum length of 65535.
    Message : Optional[str]
        The error message associated with the PartiQL batch response.
    """

    Code: str | None = None
    Item: AttributeValueDict | None = None
    Message: str | None = None
