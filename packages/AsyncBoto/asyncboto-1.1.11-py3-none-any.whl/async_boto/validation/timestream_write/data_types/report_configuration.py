from pydantic import BaseModel

from .report_s3_configuration import ReportS3Configuration as ReportS3ConfigurationModel


class ReportConfiguration(BaseModel):
    """
    Report configuration for a batch load task. This contains details about where error
    reports are stored.

    Attributes
    ----------
    ReportS3Configuration : ReportS3Configuration | None
        Configuration of an S3 location to write error reports and events for a
        batch load.
    """

    ReportS3Configuration: ReportS3ConfigurationModel | None = None
