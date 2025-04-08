from typing import Literal

from pydantic import BaseModel, constr


class KeySchemaElement(BaseModel):
    """
    Represents a single element of a key schema.

    Attributes
    ----------
    AttributeName : str
        The name of a key attribute.
    KeyType : Literal['HASH', 'RANGE']
        The role that this key attribute will assume.
    """

    AttributeName: constr(min_length=1, max_length=255)
    KeyType: Literal["HASH", "RANGE"]
