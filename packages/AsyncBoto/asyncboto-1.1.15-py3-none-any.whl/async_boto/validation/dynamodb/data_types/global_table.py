# ruff: noqa: E501
from pydantic import BaseModel, constr

from .replica import Replica


class GlobalTable(BaseModel):
    """
    Represents the properties of a global table.

    Attributes
    ----------
    GlobalTableName : Optional[constr(min_length=3, max_length=255, regex=r'[a-zA-Z0-9_.-]+')]
        The global table name.
    ReplicationGroup : Optional[List[Replica]]
        The Regions where the global table has replicas.
    """

    GlobalTableName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None
    ReplicationGroup: list[Replica] | None = None
