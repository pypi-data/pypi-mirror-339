from pydantic import BaseModel, constr

from .data_types.database import Database
from .data_types.tag import Tag


class CreateDatabaseRequest(BaseModel):
    """
    Creates a new Timestream database. If the AWS KMS key is not specified,
    the database will be encrypted with a Timestream managed AWS KMS key located
    in your account.

    Attributes
    ----------
    DatabaseName : str
        The name of the Timestream database.
    KmsKeyId : str | None
        The AWS KMS key for the database.
    Tags : List[Tag] | None
        A list of key-value pairs to label the table.
    """

    DatabaseName: constr(min_length=3, max_length=256, pattern=r"[a-zA-Z0-9_.-]+")
    KmsKeyId: constr(min_length=1, max_length=2048) | None = None
    Tags: list[Tag] | None = None


class CreateDatabaseResponse(BaseModel):
    """
    The response returned by the service when a CreateDatabase action is successful.

    Attributes
    ----------
    Database : Database
        The newly created Timestream database.
    """

    Database: Database
