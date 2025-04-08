from pydantic import BaseModel

from .data_types.endpoint import Endpoint


class DescribeEndpointsRequest(BaseModel):
    """
    Returns a list of available endpoints to make Timestream API calls against.
    This API is available through both Write and Query.

    It is not recommended to use this API unless:
    * You are using VPC endpoints (AWS PrivateLink) with Timestream
    * Your application uses a programming language that does not yet have SDK support
    * You require better control over the client-side implementation
    """

    pass


class DescribeEndpointsResponse(BaseModel):
    """
    The response returned by the service when a DescribeEndpoints action is successful.

    Parameters
    ----------
    Endpoints : List[Endpoint]
        An Endpoints object is returned when a DescribeEndpoints request is made.
    """

    Endpoints: list[Endpoint]
