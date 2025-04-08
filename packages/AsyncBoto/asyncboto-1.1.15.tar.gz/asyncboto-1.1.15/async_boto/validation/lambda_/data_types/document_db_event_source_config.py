from typing import Literal

from pydantic import BaseModel, Field


class DocumentDBEventSourceConfig(BaseModel):
    """
    Specific configuration settings for an Amazon DocumentDB event source.

    This configuration controls how Lambda connects to and processes change events
    from a DocumentDB cluster's change stream.

    Parameters
    ----------
    CollectionName : Optional[str]
        The name of the collection to consume within the DocumentDB database.

        If specified, Lambda will only receive change events from this specific
        collection. If not specified, Lambda consumes all collections within the
        specified database.

        Constraints:
        - Must not start with "system." (reserved prefix)
        - Must start with a letter or underscore
        - Min length: 1
        - Max length: 57
        - Pattern: (^(?!(system\x2e)))(^[_a-zA-Z0-9])([^$]*)

    DatabaseName : Optional[str]
        The name of the database to consume within the DocumentDB cluster.

        This parameter is required when creating a DocumentDB event source mapping.
        All changes from collections within this database (or the specific collection
        if CollectionName is provided) will be sent to the Lambda function.

        Constraints:
        - Cannot contain spaces, slash, dot, dollar sign, or double quotes
        - Min length: 1
        - Max length: 63
        - Pattern: [^ /\\.$\x22]*

    FullDocument : Optional[Literal["UpdateLookup", "Default"]]
        Determines what DocumentDB sends to your event stream during document update
        operations.

        Options:
        - "UpdateLookup": DocumentDB sends a delta describing the changes, along with
        a copy
          of the entire document. This provides more context but increases the event
          size.
        - "Default": DocumentDB sends only a partial document that contains the changes.
          This is more efficient but provides less context.
    """

    CollectionName: str | None = Field(
        None,
        min_length=1,
        max_length=57,
    )
    DatabaseName: str | None = Field(None, min_length=1, max_length=63)
    FullDocument: Literal["UpdateLookup", "Default"] | None = None
