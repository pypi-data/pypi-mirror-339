# ruff: noqa: E501
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, constr

from .replica_description import ReplicaDescription


class GlobalTableDescription(BaseModel):
    """
    Contains details about the global table.

    Attributes
    ----------
    CreationDateTime : Optional[datetime]
        The creation time of the global table.
    GlobalTableArn : Optional[str]
        The unique identifier of the global table.
    GlobalTableName : Optional[constr(min_length=3, max_length=255, regex=r'[a-zA-Z0-9_.-]+')]
        The global table name.
    GlobalTableStatus : Optional[Literal['CREATING', 'ACTIVE', 'DELETING', 'UPDATING']]
        The current state of the global table.
    ReplicationGroup : Optional[List[ReplicaDescription]]
        The Regions where the global table has replicas.
    """

    CreationDateTime: datetime | None = None
    GlobalTableArn: str | None = None
    GlobalTableName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None
    GlobalTableStatus: Literal["CREATING", "ACTIVE", "DELETING", "UPDATING"] | None = (
        None
    )
    ReplicationGroup: list[ReplicaDescription] | None = None
