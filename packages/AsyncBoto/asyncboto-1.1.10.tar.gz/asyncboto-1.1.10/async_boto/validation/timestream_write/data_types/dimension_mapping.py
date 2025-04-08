from pydantic import BaseModel, constr


class DimensionMapping(BaseModel):
    """
    Represents the mapping of dimension columns.

    Attributes
    ----------
    DestinationColumn : str | None
        The destination column of the dimension mapping.
    SourceColumn : str | None
        The source column of the dimension mapping.
    """

    DestinationColumn: constr(min_length=1) | None = None
    SourceColumn: constr(min_length=1) | None = None
