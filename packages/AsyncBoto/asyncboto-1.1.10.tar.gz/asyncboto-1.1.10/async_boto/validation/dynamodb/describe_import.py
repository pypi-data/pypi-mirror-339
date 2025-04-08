from pydantic import BaseModel, constr

from .data_types.import_table_description import (
    ImportTableDescription as ImportTableDescriptionModel,
)


class DescribeImportRequest(BaseModel):
    """
    Represents the properties of the import.

    Attributes
    ----------
    ImportArn : str
        The Amazon Resource Name (ARN) associated with the table you're importing to.
    """

    ImportArn: constr(min_length=37, max_length=1024)


class DescribeImportResponse(BaseModel):
    """
    Response for the DescribeImport operation.

    Attributes
    ----------
    ImportTableDescription : Optional[ImportTableDescription]
        Represents the properties of the table created for the import, and
        parameters of the import.
    """

    ImportTableDescription: ImportTableDescriptionModel | None = None
