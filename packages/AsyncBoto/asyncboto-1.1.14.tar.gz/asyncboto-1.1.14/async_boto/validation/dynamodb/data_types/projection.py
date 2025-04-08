from typing import Literal

from pydantic import BaseModel, conlist, constr


class Projection(BaseModel):
    """
    Represents attributes that are copied (projected) from the table into an index.

    Attributes
    ----------
    NonKeyAttributes : Optional[List[str]]
        Represents the non-key attribute names which will be projected into the index.
    ProjectionType : Optional[str]
        The set of attributes that are projected into the index.
    """

    NonKeyAttributes: (
        conlist(constr(min_length=1, max_length=255), min_length=1, max_length=20)
        | None
    ) = None  # noqa: E501
    ProjectionType: Literal["ALL", "KEYS_ONLY", "INCLUDE"] | None = None
