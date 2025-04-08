from pydantic import BaseModel


class CreateReplicaAction(BaseModel):
    """
    Represents a replica to be added.

    Attributes
    ----------
    RegionName : str
        The Region of the replica to be added.
    """

    RegionName: str
