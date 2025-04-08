from pydantic import BaseModel, constr


class CsvConfiguration(BaseModel):
    """
    A delimited data format where the column separator can be a comma and the record
    separator is a newline character.

    Attributes
    ----------
    ColumnSeparator : str | None
        Column separator can be one of comma (','), pipe ('|'), semicolon (';'),
        tab ('\t'), or blank space (' ').
    EscapeChar : str | None
        Escape character.
    NullValue : str | None
        Can be blank space (' ').
    QuoteChar : str | None
        Can be single quote (') or double quote (").
    TrimWhiteSpace : bool | None
        Specifies to trim leading and trailing white space.
    """

    ColumnSeparator: constr(min_length=1, max_length=1) | None = None
    EscapeChar: constr(min_length=1, max_length=1) | None = None
    NullValue: constr(min_length=1, max_length=256) | None = None
    QuoteChar: constr(min_length=1, max_length=1) | None = None
    TrimWhiteSpace: bool | None = None
