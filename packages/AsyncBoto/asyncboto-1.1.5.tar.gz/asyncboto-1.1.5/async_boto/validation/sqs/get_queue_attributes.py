from pydantic import BaseModel


class GetQueueAttributesRequest(BaseModel):
    """
    The request accepts the following data in JSON format.

    Attributes
    ----------
    AttributeNames : Optional[List[str]]
        A list of attributes for which to retrieve information.
    QueueUrl : str
        The URL of the Amazon SQS queue whose attribute information is retrieved.
    """

    AttributeNames: list[str] | None = None
    QueueUrl: str


class GetQueueAttributesResponse(BaseModel):
    """
    The response returned in JSON format by the service.

    Attributes
    ----------
    Attributes : Dict[str, str]
        A map of attributes to their respective values.
    """

    Attributes: dict[str, str]
