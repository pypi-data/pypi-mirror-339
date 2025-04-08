from pydantic import BaseModel, conlist, constr

from .key_schema_element import KeySchemaElement
from .projection import Projection as ProjectionModel


class LocalSecondaryIndexDescription(BaseModel):
    """
    Represents the properties of a local secondary index.

    Attributes
    ----------
    IndexArn : Optional[str]
        The Amazon Resource Name (ARN) that uniquely identifies the index.
    IndexName : Optional[str]
        Represents the name of the local secondary index.
    IndexSizeBytes : Optional[int]
        The total size of the specified index, in bytes.
    ItemCount : Optional[int]
        The number of items in the specified index.
    KeySchema : Optional[List[KeySchemaElement]]
        The complete key schema for the local secondary index.
    Projection : Optional[ProjectionModel]
        Represents attributes that are copied (projected) from the table into the
        global secondary index.
    """

    IndexArn: str | None = None
    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    IndexSizeBytes: int | None = None
    ItemCount: int | None = None
    KeySchema: conlist(KeySchemaElement, min_length=1, max_length=2) | None = None
    Projection: ProjectionModel | None = None
