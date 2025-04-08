from pydantic import BaseModel, constr

from .data_types.batch_load_task_description import BatchLoadTaskDescription


class DescribeBatchLoadTaskRequest(BaseModel):
    """
    Returns information about the batch load task, including configurations,
    mappings, progress, and other details.

    Attributes
    ----------
    TaskId : str
        The ID of the batch load task.
    """

    TaskId: constr(min_length=3, max_length=32, pattern=r"[A-Z0-9]+")


class DescribeBatchLoadTaskResponse(BaseModel):
    """
    The response returned by the service when a DescribeBatchLoadTask action
    is successful.

    Attributes
    ----------
    BatchLoadTaskDescription : BatchLoadTaskDescription
        Description of the batch load task.
    """

    BatchLoadTaskDescription: BatchLoadTaskDescription
