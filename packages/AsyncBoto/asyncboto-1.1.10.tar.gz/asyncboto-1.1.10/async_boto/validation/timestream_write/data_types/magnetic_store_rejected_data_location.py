from pydantic import BaseModel

from .s3_configuration import S3Configuration as S3ConfigurationModel


class MagneticStoreRejectedDataLocation(BaseModel):
    """
    The location to write error reports for records rejected, asynchronously,
    during magnetic store writes.

    Attributes
    ----------
    S3Configuration : S3Configuration | None
        Configuration of an S3 location to write error reports for records rejected,
        asynchronously, during magnetic store writes.
    """

    S3Configuration: S3ConfigurationModel | None = None
