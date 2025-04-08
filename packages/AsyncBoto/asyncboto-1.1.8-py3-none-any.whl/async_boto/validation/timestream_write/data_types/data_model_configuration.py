from pydantic import BaseModel

from .data_model import DataModel as DataModelModel
from .data_model_s3_configuration import (
    DataModelS3Configuration as DataModelS3ConfigurationModel,
)


class DataModelConfiguration(BaseModel):
    """
    Data model configuration for a batch load task.

    Attributes
    ----------
    DataModel : DataModel | None
        Data model for a batch load task.
    DataModelS3Configuration : DataModelS3Configuration | None
        S3 configuration for the data model.
    """

    DataModel: DataModelModel | None = None
    DataModelS3Configuration: DataModelS3ConfigurationModel | None = None
