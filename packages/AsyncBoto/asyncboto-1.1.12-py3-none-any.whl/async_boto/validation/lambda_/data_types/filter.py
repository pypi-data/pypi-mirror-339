from typing import Annotated

from pydantic import BaseModel, Field


class Filter(BaseModel):
    """
    A structure within a FilterCriteria object that defines an event filtering pattern.

    Parameters
    ----------
    Pattern : Optional[str], optional
        A filter pattern for event filtering. Follows Lambda event filtering syntax.
    """

    Pattern: Annotated[str | None, Field(max_length=4096)] = None
