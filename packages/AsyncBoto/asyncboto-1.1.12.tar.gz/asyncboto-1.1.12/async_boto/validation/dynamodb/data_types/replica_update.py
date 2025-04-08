from pydantic import BaseModel

from .create_replica_action import CreateReplicaAction
from .delete_replica_action import DeleteReplicaAction


class ReplicaUpdate(BaseModel):
    """
    Represents one of the following:
    - A new replica to be added to an existing global table.
    - New parameters for an existing replica.
    - An existing replica to be removed from an existing global table.

    Attributes
    ----------
    Create : Optional[CreateReplicaAction]
        The parameters required for creating a replica on an existing global table.
    Delete : Optional[DeleteReplicaAction]
        The name of the existing replica to be removed.
    """

    Create: CreateReplicaAction | None = None
    Delete: DeleteReplicaAction | None = None
