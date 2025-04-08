# snap_start.py
from typing import Literal

from pydantic import BaseModel


class SnapStart(BaseModel):
    """
    The function's Lambda SnapStart setting. Set ApplyOn to PublishedVersions
    to create a snapshot of the initialized execution environment when you
    publish a function version.

    Parameters
    ----------
    ApplyOn : Literal["PublishedVersions", "None"], optional
        Set to PublishedVersions to create a snapshot of the initialized
        execution environment when you publish a function version.
    """

    ApplyOn: Literal["PublishedVersions", "None"] | None = None
