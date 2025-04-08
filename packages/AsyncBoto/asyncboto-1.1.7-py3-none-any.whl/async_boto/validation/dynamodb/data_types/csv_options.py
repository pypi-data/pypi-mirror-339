# ruff: noqa: E501
from pydantic import BaseModel, conlist, constr


class CsvOptions(BaseModel):
    """
    Processing options for the CSV file being imported.

    Attributes
    ----------
    Delimiter : Optional[constr(min_length=1, max_length=1, pattern=r"[,;:|\t ]")]
        The delimiter used for separating items in the CSV file being imported.
    HeaderList : Optional[conlist(constr(min_length=1, max_length=65536, pattern=r"[\x20-\x21\x23-\x2b\x2d-\x7e]*"), min_items=1, max_items=255)]
        List of the headers used to specify a common header for all source CSV files being imported.
    """

    Delimiter: constr(min_length=1, max_length=1, pattern=r"[,;:|\t ]") | None = None
    HeaderList: (
        conlist(
            constr(
                min_length=1,
                max_length=65536,
                pattern=r"[\x20-\x21\x23-\x2B\x2D-\x7E]*",
            ),
            min_length=1,
            max_length=255,
        )
        | None
    ) = None
