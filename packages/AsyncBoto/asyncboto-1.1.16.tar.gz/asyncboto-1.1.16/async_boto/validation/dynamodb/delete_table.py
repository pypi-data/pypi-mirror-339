from pydantic import BaseModel, constr

from .data_types.table_description import TableDescription as TableDescriptionModel


class DeleteTableRequest(BaseModel):
    """
    Deletes a table and all of its items.

    Attributes
    ----------
    TableName : str
        The name of the table to delete.
    """

    TableName: constr(min_length=3, max_length=1024)


class DeleteTableResponse(BaseModel):
    """
    Response for the DeleteTable operation.

    Attributes
    ----------
    TableDescription : TableDescription
        Represents the properties of the table.
    """

    TableDescription: TableDescriptionModel = None
