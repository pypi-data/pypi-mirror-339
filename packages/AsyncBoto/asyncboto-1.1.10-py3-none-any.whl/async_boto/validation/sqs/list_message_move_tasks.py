from pydantic import BaseModel, conint

from .data_types.list_message_move_tasks_result_entry import (
    ListMessageMoveTasksResultEntry,
)


class ListMessageMoveTasksRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    MaxResults : Optional[int]
        The maximum number of results to include in the response.
    SourceArn : str
        The ARN of the queue whose message movement tasks are to be listed.
    """

    MaxResults: conint(ge=1, le=10) | None = None
    SourceArn: str


class ListMessageMoveTasksResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    Results : List[ListMessageMoveTasksResultEntry]
        A list of message movement tasks and their attributes.
    """

    Results: list[ListMessageMoveTasksResultEntry]
