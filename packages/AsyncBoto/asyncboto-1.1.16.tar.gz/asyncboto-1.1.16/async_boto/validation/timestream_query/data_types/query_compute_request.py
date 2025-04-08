from typing import Literal

from pydantic import BaseModel

from .provisioned_capacity_request import ProvisionedCapacityRequest


class QueryComputeRequest(BaseModel):
    """
    A request to retrieve or update the compute capacity settings for querying data.
    QueryCompute is available only in the Asia Pacific (Mumbai) region.

    Parameters
    ----------
    ComputeMode : Optional[str]
        The mode in which Timestream Compute Units (TCUs) are allocated and utilized
        within an account.
        Note that in the Asia Pacific (Mumbai) region, the API operation only recognizes
        the value `PROVISIONED`. QueryCompute is available only in the Asia Pacific
        (Mumbai) region.
    ProvisionedCapacity : Optional[ProvisionedCapacityRequest]
        Configuration object that contains settings for provisioned Timestream
        Compute Units (TCUs)
        in your account. QueryCompute is available only in the Asia Pacific
        (Mumbai) region.
    """

    ComputeMode: Literal["ON_DEMAND", "PROVISIONED"] | None = None
    ProvisionedCapacity: ProvisionedCapacityRequest | None = None
