from pydantic import BaseModel, conlist, constr

from .key_schema_element import KeySchemaElement
from .projection import Projection as ProjectionModel


class LocalSecondaryIndex(BaseModel):
    """
    Represents the properties of a local secondary index.

    Attributes
    ----------
    IndexName : str
        The name of the local secondary index.
    KeySchema : List[KeySchemaElement]
        The complete key schema for the local secondary index.
    Projection : Projection
        Represents attributes that are copied (projected) from the table into the
        local secondary index.
    """

    IndexName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
    KeySchema: conlist(KeySchemaElement, min_length=1, max_length=2)
    Projection: ProjectionModel
