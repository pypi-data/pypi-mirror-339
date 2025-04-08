from pydantic import BaseModel


class BatchResultErrorEntry(BaseModel):
    """
    Represents the result of an action on each entry in a batch request.

    Attributes
    ----------
    Code : str
        An error code representing why the action failed on this entry.
    Id : str
        The Id of an entry in a batch request.
    SenderFault : bool
        Specifies whether the error happened due to the caller of the batch API action.
    Message : str, optional
        A message explaining why the action failed on this entry.
    """

    Code: str
    Id: str
    SenderFault: bool
    Message: str = None
