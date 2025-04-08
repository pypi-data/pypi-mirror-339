from pydantic import BaseModel, constr


class DeleteTableRequest(BaseModel):
    """
    Deletes a given Timestream table. This is an irreversible operation.
    After a Timestream database table is deleted, the time-series data
    stored in the table cannot be recovered.

    Attributes
    ----------
    DatabaseName : str
        The name of the database where the Timestream database is to be deleted.
    TableName : str
        The name of the Timestream table to be deleted.
    """

    DatabaseName: constr(min_length=3, max_length=256)
    TableName: constr(min_length=3, max_length=256)


class DeleteTableResponse(BaseModel):
    pass
