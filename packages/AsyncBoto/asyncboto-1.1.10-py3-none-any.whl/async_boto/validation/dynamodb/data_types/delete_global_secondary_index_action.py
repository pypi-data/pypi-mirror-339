from pydantic import BaseModel, constr


class DeleteGlobalSecondaryIndexAction(BaseModel):
    """
    Represents a global secondary index to be deleted from an existing table.

    Attributes
    ----------
    IndexName : constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
        The name of the global secondary index to be deleted.
    """

    IndexName: constr(min_length=3, max_length=255, pattern=r"[a-zA-Z0-9_.-]+")
