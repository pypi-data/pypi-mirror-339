from pydantic import BaseModel, constr

from .data_types.global_table_description import (
    GlobalTableDescription as GlobalTableDescriptionModel,
)
from .data_types.replica_update import ReplicaUpdate


class UpdateGlobalTableRequest(BaseModel):
    """
    Request model for the UpdateGlobalTable operation.

    Attributes
    ----------
    GlobalTableName : str
        The global table name.
    ReplicaUpdates : List[ReplicaUpdate]
        A list of regions that should be added or removed from the global table.
    """

    GlobalTableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    ReplicaUpdates: list[ReplicaUpdate]


class UpdateGlobalTableResponse(BaseModel):
    """
    Response model for the UpdateGlobalTable operation.

    Attributes
    ----------
    GlobalTableDescription : GlobalTableDescription
        Contains the details of the global table.
    """

    GlobalTableDescription: GlobalTableDescriptionModel | None = None
