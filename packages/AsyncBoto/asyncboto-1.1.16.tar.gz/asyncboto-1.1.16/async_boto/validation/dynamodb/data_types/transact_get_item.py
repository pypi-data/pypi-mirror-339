from pydantic import BaseModel

from .get import Get as GetModel


class TransactGetItem(BaseModel):
    """
    Specifies an item to be retrieved as part of the transaction.

    Attributes
    ----------
    Get : Get
        Contains the primary key that identifies the item to get,
        together with the name of the table that contains the item,
        and optionally the specific attributes of the item to retrieve.
    """

    Get: GetModel
