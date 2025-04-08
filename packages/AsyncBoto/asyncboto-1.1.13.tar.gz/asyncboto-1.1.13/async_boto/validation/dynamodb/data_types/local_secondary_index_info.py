from pydantic import BaseModel, conlist, constr

from .key_schema_element import KeySchemaElement
from .projection import Projection as ProjectionModel


class LocalSecondaryIndexInfo(BaseModel):
    """
    Represents the properties of a local secondary index for the table when the
    backup was created.

    Attributes
    ----------
    IndexName : Optional[str]
        Represents the name of the local secondary index.
    KeySchema : Optional[List[KeySchemaElement]]
        The complete key schema for a local secondary index.
    Projection : Optional[ProjectionModel]
        Represents attributes that are copied (projected) from the table into the
        global secondary index.
    """

    IndexName: (
        constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+") | None
    ) = None  # noqa: E501
    KeySchema: conlist(KeySchemaElement, min_length=1, max_length=2) | None = None
    Projection: ProjectionModel | None = None
