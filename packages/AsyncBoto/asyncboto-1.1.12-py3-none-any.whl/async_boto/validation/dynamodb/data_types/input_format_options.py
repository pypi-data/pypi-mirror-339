from pydantic import BaseModel

from .csv_options import CsvOptions


class InputFormatOptions(BaseModel):
    """
    The format options for the data that was imported into the target table.

    Attributes
    ----------
    Csv : Optional[CsvOptions]
        The options for imported source files in CSV format.
    """

    Csv: CsvOptions | None = None
