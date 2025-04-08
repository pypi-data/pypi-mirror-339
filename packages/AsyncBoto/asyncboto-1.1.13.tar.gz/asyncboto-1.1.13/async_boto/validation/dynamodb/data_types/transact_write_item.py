from pydantic import BaseModel

from .condition_check import ConditionCheck as ConditionCheckModel
from .delete import Delete as DeleteModel
from .put import Put as PutModel
from .update import Update as UpdateModel


class TransactWriteItem(BaseModel):
    """
    A list of requests that can perform update, put, delete, or check operations on
    multiple items in one or more tables atomically.

    Attributes
    ----------
    ConditionCheck : Optional[ConditionCheck]
        A request to perform a check item operation.
    Delete : Optional[Delete]
        A request to perform a DeleteItem operation.
    Put : Optional[Put]
        A request to perform a PutItem operation.
    Update : Optional[Update]
        A request to perform an UpdateItem operation.
    """

    ConditionCheck: ConditionCheckModel | None = None
    Delete: DeleteModel | None = None
    Put: PutModel | None = None
    Update: UpdateModel | None = None
