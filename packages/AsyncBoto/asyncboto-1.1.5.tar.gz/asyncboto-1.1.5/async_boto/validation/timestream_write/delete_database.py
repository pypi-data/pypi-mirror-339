from pydantic import BaseModel, constr


class DeleteDatabaseRequest(BaseModel):
    """
    Deletes a given Timestream database. This is an irreversible operation.
    After a database is deleted, the time-series data from its tables
    cannot be recovered.

    Attributes
    ----------
    DatabaseName : str
        The name of the Timestream database to be deleted.
    """

    DatabaseName: constr(min_length=3, max_length=256)


class DeleteDatabaseResponse(BaseModel):
    pass
