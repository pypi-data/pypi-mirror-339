from pydantic import BaseModel

from .create_replication_group_member_action import CreateReplicationGroupMemberAction
from .delete_replication_group_member_action import DeleteReplicationGroupMemberAction
from .update_replication_group_member_action import UpdateReplicationGroupMemberAction


class ReplicationGroupUpdate(BaseModel):
    """
    Represents one of the following:
    - A new replica to be added to an existing regional table or global table.
    - New parameters for an existing replica.
    - An existing replica to be deleted.

    Attributes
    ----------
    Create : Optional[CreateReplicationGroupMemberAction]
        The parameters required for creating a replica for the table.
    Delete : Optional[DeleteReplicationGroupMemberAction]
        The parameters required for deleting a replica for the table.
    Update : Optional[UpdateReplicationGroupMemberAction]
        The parameters required for updating a replica for the table.
    """

    Create: CreateReplicationGroupMemberAction | None = None
    Delete: DeleteReplicationGroupMemberAction | None = None
    Update: UpdateReplicationGroupMemberAction | None = None
