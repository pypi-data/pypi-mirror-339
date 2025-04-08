from typing import Literal

from pydantic import BaseModel

from .provisioned_capacity_response import ProvisionedCapacityResponse


class QueryComputeResponse(BaseModel):
    """
    The response to a request to retrieve or update the compute capacity settings
    for querying data.

    QueryCompute is available only in the Asia Pacific (Mumbai) region.

    Parameters
    ----------
    ComputeMode : Optional[ComputeMode]
        The mode in which Timestream Compute Units (TCUs) are allocated and utilized
        within an account.
        Note that in the Asia Pacific (Mumbai) region, the API operation only
        recognizes the value
        `PROVISIONED`.
    ProvisionedCapacity : Optional[ProvisionedCapacityResponse]
        Configuration object that contains settings for provisioned Timestream
        Compute Units (TCUs)
        in your account.
    """

    ComputeMode: Literal["ON_DEMAND", "PROVISIONED"] | None = None
    ProvisionedCapacity: ProvisionedCapacityResponse | None = None
