from pydantic import BaseModel, constr


class ResumeBatchLoadTaskRequest(BaseModel):
    """
    The request to resume a batch load task.

    Attributes
    ----------
    TaskId : str
        The ID of the batch load task to resume.
    """

    TaskId: constr(min_length=3, max_length=32, pattern=r"[A-Z0-9]+")


class ResumeBatchLoadTaskResponse(BaseModel):
    pass
