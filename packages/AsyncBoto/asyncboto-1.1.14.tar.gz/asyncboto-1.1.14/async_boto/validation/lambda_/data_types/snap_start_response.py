# snap_start_response.py
from typing import Literal

from pydantic import BaseModel


class SnapStartResponse(BaseModel):
    """
    The function's SnapStart setting.

    Parameters
    ----------
    ApplyOn : Literal["PublishedVersions", "None"], optional
        When set to PublishedVersions, Lambda creates a snapshot of the
        execution environment when you publish a function version.
    OptimizationStatus : Literal["On", "Off"], optional
        When you provide a qualified Amazon Resource Name (ARN), this
        response element indicates whether SnapStart is activated for
        the specified function version.
    """

    ApplyOn: Literal["PublishedVersions", "None"] | None = None
    OptimizationStatus: Literal["On", "Off"] | None = None
