from pydantic import BaseModel, conint, constr

from .data_types.global_table import GlobalTable


class ListGlobalTablesRequest(BaseModel):
    """
    Request model for the ListGlobalTables operation.

    Attributes
    ----------
    ExclusiveStartGlobalTableName : Optional[str]
        The first global table name that this operation will evaluate.
    Limit : Optional[int]
        The maximum number of table names to return.
    RegionName : Optional[str]
        Lists the global tables in a specific Region.
    """

    ExclusiveStartGlobalTableName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    Limit: conint(ge=1) | None = None
    RegionName: str | None = None


class ListGlobalTablesResponse(BaseModel):
    """
    Response model for the ListGlobalTables operation.

    Attributes
    ----------
    GlobalTables : Optional[List[GlobalTable]]
        List of global table names.
    LastEvaluatedGlobalTableName : Optional[str]
        Last evaluated global table name.
    """

    GlobalTables: list[GlobalTable] | None = None
    LastEvaluatedGlobalTableName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
