from typing import Literal

from pydantic import BaseModel, constr

from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel
from .data_types.item_response import ItemResponse
from .data_types.parametrized_statement import ParameterizedStatement


class ExecuteTransactionRequest(BaseModel):
    """
    Allows you to perform transactional reads or writes on data stored in DynamoDB,
    using PartiQL.

    Attributes
    ----------
    TransactStatements : List[ParameterizedStatement]
        The list of PartiQL statements representing the transaction to run.
    ClientRequestToken : Optional[str]
        Set this value to get remaining results, if NextToken was returned in the
        statement response.
    ReturnConsumedCapacity : Optional[Literal['INDEXES', 'TOTAL', 'NONE']]
        Determines the level of detail about either provisioned or on-demand
        throughput consumption that is returned in the response.
    """

    TransactStatements: list[ParameterizedStatement]
    ClientRequestToken: constr(min_length=1, max_length=36) | None = None
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None


class ExecuteTransactionResponse(BaseModel):
    """
    Response for the ExecuteTransaction operation.

    Attributes
    ----------
    ConsumedCapacity : Optional[List[ConsumedCapacity]]
        The capacity units consumed by the entire operation.
    Responses : Optional[List[ItemResponse]]
        The response to a PartiQL transaction.
    """

    ConsumedCapacity: list[ConsumedCapacityModel] | None = None
    Responses: list[ItemResponse] | None = None
