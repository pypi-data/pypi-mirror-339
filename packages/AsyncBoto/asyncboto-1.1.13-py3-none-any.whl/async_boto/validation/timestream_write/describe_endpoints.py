from pydantic import BaseModel

from .data_types.endpoint import Endpoint


class DescribeEndpointsResponse(BaseModel):
    """
    The response returned by the service when a DescribeEndpoints action is successful.

    Attributes
    ----------
    Endpoints : List[Endpoint]
        A list of available endpoints to make Timestream API calls against.
    """

    Endpoints: list[Endpoint]
