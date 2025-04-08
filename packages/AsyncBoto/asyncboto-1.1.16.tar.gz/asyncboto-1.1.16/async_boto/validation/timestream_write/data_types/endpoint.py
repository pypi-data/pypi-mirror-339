from pydantic import BaseModel


class Endpoint(BaseModel):
    """
    Represents an available endpoint against which to make API calls,
    as well as the TTL for that endpoint.

    Attributes
    ----------
    Address : str
        An endpoint address.
    CachePeriodInMinutes : int
        The TTL for the endpoint, in minutes.
    """

    Address: str
    CachePeriodInMinutes: int
