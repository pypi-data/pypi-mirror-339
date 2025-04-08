from pydantic import BaseModel


class ChangeMessageVisibilityBatchRequestEntry(BaseModel):
    """
    Encloses a receipt handle and an entry ID for each message in
    ChangeMessageVisibilityBatch.

    Attributes
    ----------
    Id : str
        An identifier for this particular receipt handle used to communicate the result.
        This identifier can have up to 80 characters. The following characters are
        accepted: alphanumeric characters, hyphens(-), and underscores (_).
    ReceiptHandle : str
        A receipt handle.
    VisibilityTimeout : int, optional
        The new value (in seconds) for the message's visibility timeout.
    """

    Id: str
    ReceiptHandle: str
    VisibilityTimeout: int = None
