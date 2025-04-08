from typing import Literal

from pydantic import BaseModel, constr

from .data_types.import_table_description import (
    ImportTableDescription as ImportTableDescriptionModel,
)
from .data_types.input_format_options import (
    InputFormatOptions as InputFormatOptionsModel,
)
from .data_types.s3_bucket_source import S3BucketSource as S3BucketSourceModel
from .data_types.table_creation_parameters import (
    TableCreationParameters as TableCreationParametersModel,
)


class ImportTableRequest(BaseModel):
    """
    Request model for the ImportTable operation.

    Attributes
    ----------
    InputFormat : Literal['CSV', 'DYNAMODB_JSON', 'ION']
        The format of the source data.
    S3BucketSource : S3BucketSource
        The S3 bucket that provides the source for the import.
    TableCreationParameters : TableCreationParameters
        Parameters for the table to import the data into.
    ClientToken : Optional[str]
        Providing a ClientToken makes the call idempotent.
    InputCompressionType : Optional[Literal['GZIP', 'ZSTD', 'NONE']]
        Type of compression to be used on the input coming from the imported table.
    InputFormatOptions : Optional[InputFormatOptions]
        Additional properties that specify how the input is formatted.
    """

    InputFormat: Literal["CSV", "DYNAMODB_JSON", "ION"]
    S3BucketSource: S3BucketSourceModel
    TableCreationParameters: TableCreationParametersModel
    ClientToken: constr(pattern=r"^[^\$]+$") | None = None
    InputCompressionType: Literal["GZIP", "ZSTD", "NONE"] | None = None
    InputFormatOptions: InputFormatOptionsModel | None = None


class ImportTableResponse(BaseModel):
    """
    Response model for the ImportTable operation.

    Attributes
    ----------
    ImportTableDescription : Optional[ImportTableDescription]
        Represents the properties of the table created for the import, and parameters
        of the import.
    """

    ImportTableDescription: ImportTableDescriptionModel | None = None
