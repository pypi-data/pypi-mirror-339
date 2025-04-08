from pydantic import BaseModel, constr

from .data_types.parameter_mapping import ParameterMapping
from .data_types.select_column import SelectColumn


class PrepareQueryRequest(BaseModel):
    """
    A synchronous operation that allows you to submit a query with parameters
    to be stored by Timestream for later running. Timestream only supports
    using this operation with ValidateOnly set to true.

    Parameters
    ----------
    QueryString : str
        The Timestream query string that you want to use as a prepared statement.
        Parameter names can be specified in the query string @ character followed
        by an identifier.
    ValidateOnly : bool
        By setting this value to true, Timestream will only validate that the
        query string is a valid Timestream query, and not store the prepared
        query for later use.
    """

    QueryString: constr(min_length=1, max_length=262144)
    ValidateOnly: bool | None = None


class PrepareQueryResponse(BaseModel):
    """
    The response returned by the service when a PrepareQuery action is successful.

    Parameters
    ----------
    Columns : List[SelectColumn]
        A list of SELECT clause columns of the submitted query string.
    Parameters : List[ParameterMapping]
        A list of parameters used in the submitted query string.
    QueryString : str
        The query string that you want prepare.
    """

    Columns: list[SelectColumn]
    Parameters: list[ParameterMapping]
    QueryString: constr(min_length=1, max_length=262144)
