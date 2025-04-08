from pydantic import BaseModel


class SetQueueAttributesRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    Attributes : Dict[str, str]
        A map of attributes to set.
    QueueUrl : str
        The URL of the Amazon SQS queue whose attributes are set.
    """

    Attributes: dict[str, str]
    QueueUrl: str


class SetQueueAttributesResponse(BaseModel):
    """
    The response returned in JSON format by the service.
    """

    pass
