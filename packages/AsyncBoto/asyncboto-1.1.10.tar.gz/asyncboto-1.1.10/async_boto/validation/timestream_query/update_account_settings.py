from typing import Literal

from pydantic import BaseModel

from .data_types.query_compute_request import QueryComputeRequest
from .data_types.query_compute_response import QueryComputeResponse


class UpdateAccountSettingsRequest(BaseModel):
    """
    Transitions your account to use TCUs for query pricing and modifies the maximum
    query compute units that you've configured.

    Parameters
    ----------
    MaxQueryTCU : int
        The maximum number of compute units the service will use at
        any point in time to serve your queries.
        To run queries, you must set a minimum capacity of 4 TCU.
        You can set the maximum number of TCU
        in multiples of 4, for example, 4, 8, 16, 32, and so on.
        The maximum value supported for MaxQueryTCU
        is 1000.
    QueryCompute : QueryComputeRequest
        Modifies the query compute settings configured in your account,
        including the query pricing model
        and provisioned Timestream Compute Units (TCUs) in your account.
        QueryCompute is available only
        in the Asia Pacific (Mumbai) region.
    QueryPricingModel : str
        The pricing model for queries in an account.
    """

    MaxQueryTCU: int | None = None
    QueryCompute: QueryComputeRequest | None = None
    QueryPricingModel: Literal["BYTES_SCANNED", "COMPUTE_UNITS"] | None = None


class UpdateAccountSettingsResponse(BaseModel):
    """
    The response returned by the service when an UpdateAccountSettings
    action is successful.

    Parameters
    ----------
    MaxQueryTCU : int
        The configured maximum number of compute units the service will use at
        any point in time to serve your queries.
    QueryCompute : QueryComputeResponse
        Confirms the updated account settings for querying data in your account.
        QueryCompute is available only in the Asia Pacific (Mumbai) region.
    QueryPricingModel : str
        The pricing model for an account.
    """

    MaxQueryTCU: int
    QueryCompute: QueryComputeResponse
    QueryPricingModel: Literal["BYTES_SCANNED", "COMPUTE_UNITS"]
