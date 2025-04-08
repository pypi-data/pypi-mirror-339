from pydantic import BaseModel, constr

from .data_types.export_description import ExportDescription as ExportDescriptionModel


class DescribeExportRequest(BaseModel):
    """
    Describes an existing table export.

    Attributes
    ----------
    ExportArn : str
        The Amazon Resource Name (ARN) associated with the export.
    """

    ExportArn: constr(min_length=37, max_length=1024)


class DescribeExportResponse(BaseModel):
    """
    Response for the DescribeExport operation.

    Attributes
    ----------
    ExportDescription : Optional[ExportDescription]
        Represents the properties of the export.
    """

    ExportDescription: ExportDescriptionModel | None = None
