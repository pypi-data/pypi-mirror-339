from pydantic import BaseModel, constr

from .data_types.replica_settings_description import ReplicaSettingsDescription


class DescribeGlobalTableSettingsRequest(BaseModel):
    """
    Describes Region-specific settings for a global table.

    Attributes
    ----------
    GlobalTableName : str
        The name of the global table to describe.
    """

    GlobalTableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")


class DescribeGlobalTableSettingsResponse(BaseModel):
    """
    Response for the DescribeGlobalTableSettings operation.

    Attributes
    ----------
    GlobalTableName : str
        The name of the global table.
    ReplicaSettings : List[ReplicaSettingsDescription]
        The list of replica settings descriptions.
    """

    GlobalTableName: str
    ReplicaSettings: list[ReplicaSettingsDescription]
