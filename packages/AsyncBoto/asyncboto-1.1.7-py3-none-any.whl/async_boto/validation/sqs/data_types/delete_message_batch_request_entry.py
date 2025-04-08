from pydantic import BaseModel


class DeleteMessageBatchRequestEntry(BaseModel):
    """
    Encloses a receipt handle and an identifier for it.

    Attributes
    ----------
    Id : str
        The identifier for this particular receipt handle. This is used to communicate
        the result.
        This identifier can have up to 80 characters. The following characters
        are accepted: alphanumeric characters, hyphens(-), and underscores (_).
    ReceiptHandle : str
        A receipt handle.
    """

    Id: str
    ReceiptHandle: str
