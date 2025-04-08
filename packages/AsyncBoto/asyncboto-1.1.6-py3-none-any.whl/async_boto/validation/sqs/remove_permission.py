from pydantic import BaseModel


class RemovePermissionRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    Label : str
        The identification of the permission to remove.
    QueueUrl : str
        The URL of the Amazon SQS queue from which permissions are removed.
    """

    Label: str
    QueueUrl: str


class RemovePermissionResponse(BaseModel):
    """
    The response returned in JSON format by the service.
    """

    pass
