from pydantic import BaseModel, constr

from .data_types.database import Database


class UpdateDatabaseRequest(BaseModel):
    """
    Modifies the AWS KMS key for an existing database.

    Attributes
    ----------
    DatabaseName : str
        The name of the database.
    KmsKeyId : str
        The identifier of the new AWS KMS key to be used to encrypt the data stored
        in the database.
    """

    DatabaseName: constr(min_length=3, max_length=256)
    KmsKeyId: constr(min_length=1, max_length=2048)


class UpdateDatabaseResponse(BaseModel):
    """
    The response returned by the service when an UpdateDatabase action is successful.

    Attributes
    ----------
    Database : Database
        A top-level container for a table. Databases and tables are the fundamental
        management concepts in Amazon Timestream. All tables in a database are encrypted
         with the same AWS KMS key.
    """

    Database: Database
