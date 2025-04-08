# ruff: noqa: E501
from typing import Literal

from pydantic import BaseModel, conint

from .data_types.batch_load_task import BatchLoadTask


class ListBatchLoadTasksRequest(BaseModel):
    """
    Provides a list of batch load tasks, along with the name, status,
    when the task is resumable until, and other details.

    Attributes
    ----------
    MaxResults : Optional[int]
        The total number of items to return in the output.
    NextToken : Optional[str]
        A token to specify where to start paginating.
    TaskStatus : Optional[Literal['CREATED', 'IN_PROGRESS', 'FAILED', 'SUCCEEDED', 'PROGRESS_STOPPED', 'PENDING_RESUME']]
        Status of the batch load task.
    """

    MaxResults: conint(ge=1, le=100) | None = None
    NextToken: str | None = None
    TaskStatus: (
        Literal[
            "CREATED",
            "IN_PROGRESS",
            "FAILED",
            "SUCCEEDED",
            "PROGRESS_STOPPED",
            "PENDING_RESUME",
        ]
        | None
    ) = None


class ListBatchLoadTasksResponse(BaseModel):
    """
    The response returned by the service when a ListBatchLoadTasks action is successful.

    Attributes
    ----------
    BatchLoadTasks : List[BatchLoadTask]
        A list of batch load task details.
    NextToken : Optional[str]
        A token to specify where to start paginating.
    """

    BatchLoadTasks: list[BatchLoadTask]
    NextToken: str | None = None
