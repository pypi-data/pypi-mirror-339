from pydantic import BaseModel


class DeleteMessageBatchResultEntry(BaseModel):
    """
    Encloses the Id of an entry in DeleteMessageBatch.

    Attributes
    ----------
    Id : str
        Represents a successfully deleted message.
    """

    Id: str
