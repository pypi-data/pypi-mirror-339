from pydantic import BaseModel, Field

from .attribute_value import AttributeValueDict
from .batch_statement_error import BatchStatementError


class BatchStatementResponse(BaseModel):
    """
    A PartiQL batch statement response.

    Attributes
    ----------
    Error : Optional[BatchStatementError]
        The error associated with a failed PartiQL batch statement.
    Item : Optional[AttributeValueDict]
        A DynamoDB item associated with a BatchStatementResponse. Maximum length of
        65535.
    TableName : Optional[str]
        The table name associated with a failed PartiQL batch statement. Minimum length
        of 3. Maximum length of 255.
        Pattern: [a-zA-Z0-9_.-]+
    """

    Error: BatchStatementError | None = None
    Item: AttributeValueDict | None = None
    TableName: str | None = Field(
        None, min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+"
    )
