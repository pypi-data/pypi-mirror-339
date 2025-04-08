from pydantic import BaseModel

from .attribute_value import AttributeValueDict


class CancellationReason(BaseModel):
    """
    An ordered list of errors for each item in the request which caused the transaction
    to get cancelled.

    Attributes
    ----------
    Code : Optional[str]
        Status code for the result of the cancelled transaction.
    Item : Optional[AttributeValueDict]
        Item in the request which caused the transaction to get cancelled. Maximum
        length of 65535.
    Message : Optional[str]
        Cancellation reason message description.
    """

    Code: str | None = None
    Item: AttributeValueDict | None = None
    Message: str | None = None
