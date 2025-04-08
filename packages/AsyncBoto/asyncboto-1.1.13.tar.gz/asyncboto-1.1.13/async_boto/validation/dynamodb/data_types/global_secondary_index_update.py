from pydantic import BaseModel

from .create_global_secondary_index_action import CreateGlobalSecondaryIndexAction
from .delete_global_secondary_index_action import DeleteGlobalSecondaryIndexAction
from .update_global_secondary_index_action import UpdateGlobalSecondaryIndexAction


class GlobalSecondaryIndexUpdate(BaseModel):
    """
    Represents one of the following:
    - A new global secondary index to be added to an existing table.
    - New provisioned throughput parameters for an existing global secondary index.
    - An existing global secondary index to be removed from an existing table.

    Attributes
    ----------
    Create : Optional[CreateGlobalSecondaryIndexAction]
        The parameters required for creating a global secondary index on an existing
        table.
    Delete : Optional[DeleteGlobalSecondaryIndexAction]
        The name of an existing global secondary index to be removed.
    Update : Optional[UpdateGlobalSecondaryIndexAction]
        The name of an existing global secondary index, along with new provisioned
        throughput settings to be applied to that index.
    """

    Create: CreateGlobalSecondaryIndexAction | None = None
    Delete: DeleteGlobalSecondaryIndexAction | None = None
    Update: UpdateGlobalSecondaryIndexAction | None = None
