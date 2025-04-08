from pydantic import BaseModel


class ChangeMessageVisibilityBatchResultEntry(BaseModel):
    """
    Encloses the Id of an entry in ChangeMessageVisibilityBatch.

    Attributes
    ----------
    Id : str
        Represents a message whose visibility timeout has been changed successfully.
    """

    Id: str
