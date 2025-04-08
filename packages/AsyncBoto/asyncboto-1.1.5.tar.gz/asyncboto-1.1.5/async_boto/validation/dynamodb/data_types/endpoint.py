from pydantic import BaseModel, conint


class Endpoint(BaseModel):
    """
    An endpoint information details.

    Attributes
    ----------
    Address : str
        IP address of the endpoint.
    CachePeriodInMinutes : conint(ge=0)
        Endpoint cache time to live (TTL) value.
    """

    Address: str
    CachePeriodInMinutes: conint(ge=0)
