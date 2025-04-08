from typing import Literal

from pydantic import BaseModel

from .data_types.batch_statement_request import BatchStatementRequest
from .data_types.batch_statement_response import BatchStatementResponse
from .data_types.consumed_capacity import ConsumedCapacity as ConsumedCapacityModel


class BatchExecuteStatementRequest(BaseModel):
    Statements: list[BatchStatementRequest]
    ReturnConsumedCapacity: Literal["INDEXES", "TOTAL", "NONE"] | None = None


class BatchExecuteStatementResponse(BaseModel):
    ConsumedCapacity: list[ConsumedCapacityModel] | None = None
    Responses: list[BatchStatementResponse] | None = None
