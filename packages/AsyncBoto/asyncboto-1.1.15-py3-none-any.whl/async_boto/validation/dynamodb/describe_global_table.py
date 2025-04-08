from pydantic import BaseModel, constr

from .data_types.global_table_description import (
    GlobalTableDescription as GlobalTableDescriptionModel,
)


class DescribeGlobalTableRequest(BaseModel):
    """
    Returns information about the specified global table.

    Attributes
    ----------
    GlobalTableName : str
        The name of the global table.
    """

    GlobalTableName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")


class DescribeGlobalTableResponse(BaseModel):
    """
    Response for the DescribeGlobalTable operation.

    Attributes
    ----------
    GlobalTableDescription : Optional[GlobalTableDescription]
        Contains the details of the global table.
    """

    GlobalTableDescription: GlobalTableDescriptionModel | None = None
