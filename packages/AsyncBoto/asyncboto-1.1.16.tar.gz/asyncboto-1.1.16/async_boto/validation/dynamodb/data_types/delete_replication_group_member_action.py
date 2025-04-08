from pydantic import BaseModel


class DeleteReplicationGroupMemberAction(BaseModel):
    """
    Represents a replica to be deleted.

    Attributes
    ----------
    RegionName : str
        The Region where the replica exists.
    """

    RegionName: str
