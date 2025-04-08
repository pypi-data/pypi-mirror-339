from pydantic import BaseModel

from .s3_report_location import S3ReportLocation


class ErrorReportLocation(BaseModel):
    """
    This contains the location of the error report for a single scheduled query call.

    Attributes
    ----------
    S3ReportLocation : Optional[S3ReportLocation]
        The S3 location where error reports are written.
    """

    S3ReportLocation: S3ReportLocation | None = None
