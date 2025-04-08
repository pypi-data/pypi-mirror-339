from pydantic import BaseModel

from .filter import Filter


class FilterCriteria(BaseModel):
    """
    An object that contains the filters for an event source.

    Parameters
    ----------
    Filters : Optional[List[Filter]], optional
        A list of filters for event source mapping.
    """

    Filters: list[Filter] | None = None
