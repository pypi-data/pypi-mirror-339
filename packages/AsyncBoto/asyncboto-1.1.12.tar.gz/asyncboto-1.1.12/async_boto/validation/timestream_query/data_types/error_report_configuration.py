from pydantic import BaseModel

from .s3_configuration import S3Configuration


class ErrorReportConfiguration(BaseModel):
    """
    Configuration required for error reporting.

    Attributes
    ----------
    S3Configuration : S3Configuration
        The S3 configuration for the error reports.
    """

    S3Configuration: S3Configuration
