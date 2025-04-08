from pydantic import BaseModel, constr


class Replica(BaseModel):
    """
    Represents the properties of a replica.

    Attributes
    ----------
    RegionName : Optional[str]
        The Region where the replica needs to be created.
    """

    RegionName: constr(min_length=1) | None = None
