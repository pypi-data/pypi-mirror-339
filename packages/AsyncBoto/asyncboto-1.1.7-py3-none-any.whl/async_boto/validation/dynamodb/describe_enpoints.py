from pydantic import BaseModel

from .data_types.endpoint import Endpoint


class DescribeEndpointsResponse(BaseModel):
    Endpoints: list[Endpoint]
