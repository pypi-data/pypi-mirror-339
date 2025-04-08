from typing import Literal

from pydantic import BaseModel

from .csv_configuration import CsvConfiguration as CsvConfigurationModel
from .data_source_s3_configuration import (
    DataSourceS3Configuration as DataSourceS3ConfigurationModel,
)


class DataSourceConfiguration(BaseModel):
    """
    Defines configuration details about the data source.

    Attributes
    ----------
    DataFormat : str
        This is currently CSV.
    DataSourceS3Configuration : DataSourceS3Configuration
        Configuration of an S3 location for a file which contains data to load.
    CsvConfiguration : CsvConfiguration | None
        A delimited data format where the column separator can be a comma and the
        record separator is a newline character.
    """

    DataFormat: Literal["CSV"] = "CSV"
    DataSourceS3Configuration: DataSourceS3ConfigurationModel
    CsvConfiguration: CsvConfigurationModel | None = None
