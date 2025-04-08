from pydantic import BaseModel


class DeleteReplicaAction(BaseModel):
    """
    Represents a replica to be removed.

    Attributes
    ----------
    RegionName : str
        The Region of the replica to be removed.
    """

    RegionName: str
