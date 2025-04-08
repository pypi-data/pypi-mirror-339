from datetime import datetime

from pydantic import BaseModel, constr


class Database(BaseModel):
    """
    A top-level container for a table. Databases and tables are the fundamental
    management concepts in Amazon Timestream.
    All tables in a database are encrypted with the same AWS KMS key.

    Attributes
    ----------
    Arn : str | None
        The Amazon Resource Name that uniquely identifies this database.
    CreationTime : datetime | None
        The time when the database was created, calculated from the Unix epoch time.
    DatabaseName : str | None
        The name of the Timestream database.
    KmsKeyId : str | None
        The identifier of the AWS KMS key used to encrypt the data stored in
        the database.
    LastUpdatedTime : datetime | None
        The last time that this database was updated.
    TableCount : int | None
        The total number of tables found within a Timestream database.
    """

    Arn: str | None = None
    CreationTime: datetime | None = None
    DatabaseName: constr(min_length=3, max_length=256) | None = None
    KmsKeyId: constr(min_length=1, max_length=2048) | None = None
    LastUpdatedTime: datetime | None = None
    TableCount: int | None = None
