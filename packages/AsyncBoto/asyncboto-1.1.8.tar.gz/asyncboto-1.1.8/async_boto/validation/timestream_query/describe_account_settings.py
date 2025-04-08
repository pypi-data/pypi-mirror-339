from typing import Literal

from pydantic import BaseModel

from .data_types.query_compute_response import QueryComputeResponse


class DescribeAccountSettingsRequest(BaseModel):
    """
    Describes the settings for your account that include the query pricing model
    and the configured maximum TCUs the service can use for your query workload.

    You're charged only for the duration of compute units used for your workloads.
    """

    pass


class DescribeAccountSettingsResponse(BaseModel):
    """
    The response returned by the service when a DescribeAccountSettings action is
    successful.

    Parameters
    ----------
    MaxQueryTCU : int
        The maximum number of Timestream compute units (TCUs) the service will use at
        any point in time to serve your queries. To run queries, you must set a minimum
        capacity of 4 TCU.
        You can set the maximum number of TCU in multiples of 4, for example,
        4, 8, 16, 32, and so on.
        This configuration is applicable only for on-demand usage of (TCUs).
    QueryCompute : QueryComputeResponse
        An object that contains the usage settings for Timestream Compute Units (TCUs)
        in your account for the query workload. QueryCompute is available only in the
        Asia Pacific (Mumbai) region.
    QueryPricingModel : str
        The pricing model for queries in your account.
    """

    MaxQueryTCU: int
    QueryCompute: QueryComputeResponse
    QueryPricingModel: Literal["BYTES_SCANNED", "COMPUTE_UNITS"]
