from typing import Literal

from pydantic import BaseModel, constr

from .replica_auto_scaling_description import ReplicaAutoScalingDescription


class TableAutoScalingDescription(BaseModel):
    """
    Represents the auto scaling configuration for a global table.

    Attributes
    ----------
    Replicas : Optional[List[ReplicaAutoScalingDescription]]
        Represents replicas of the global table.
    TableName : Optional[constr(min_length=3, max_length=255)
        regex=r"^[a-zA-Z0-9_.-]+$"
        The name of the table.
    TableStatus : Optional[Literal['CREATING', 'UPDATING', 'DELETING', 'ACTIVE',
    'INACCESSIBLE_ENCRYPTION_CREDENTIALS', 'ARCHIVING', 'ARCHIVED']]
        The current state of the table.
    """

    Replicas: list[ReplicaAutoScalingDescription] | None = None
    TableName: (
        constr(min_length=3, max_length=255, pattern=r"^[a-zA-Z0-9_.-]+$") | None
    ) = None  # noqa: E501
    TableStatus: (
        Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "ACTIVE",
            "INACCESSIBLE_ENCRYPTION_CREDENTIALS",
            "ARCHIVING",
            "ARCHIVED",
        ]
        | None
    ) = None  # noqa: E501
