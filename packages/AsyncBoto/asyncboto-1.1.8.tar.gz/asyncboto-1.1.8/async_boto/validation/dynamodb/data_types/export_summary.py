from typing import Literal

from pydantic import BaseModel, constr


class ExportSummary(BaseModel):
    """
    Summary information about an export task.

    Attributes
    ----------
    ExportArn : Optional[constr(min_length=37, max_length=1024)]
        The Amazon Resource Name (ARN) of the export.
    ExportStatus : Optional[Literal["IN_PROGRESS", "COMPLETED", "FAILED"]]
        Export can be in one of the following states: IN_PROGRESS, COMPLETED, or FAILED.
    ExportType : Optional[Literal["FULL_EXPORT", "INCREMENTAL_EXPORT"]]
        The type of export that was performed.
    """

    ExportArn: constr(min_length=37, max_length=1024) | None = None
    ExportStatus: Literal["IN_PROGRESS", "COMPLETED", "FAILED"] | None = None
    ExportType: Literal["FULL_EXPORT", "INCREMENTAL_EXPORT"] | None = None
