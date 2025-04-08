from typing import Literal

from pydantic import BaseModel


class ProvisionedConcurrencyConfigListItem(BaseModel):
    """
    Details about the provisioned concurrency configuration for a function alias or
    version.

    Attributes
    ----------
    AllocatedProvisionedConcurrentExecutions : Optional[int]
        The amount of provisioned concurrency allocated.
    AvailableProvisionedConcurrentExecutions : Optional[int]
        The amount of provisioned concurrency available.
    FunctionArn : Optional[str]
        The Amazon Resource Name (ARN) of the alias or version.
    LastModified : Optional[str]
        The date and time that a user last updated the configuration,
        in ISO 8601 format.
    RequestedProvisionedConcurrentExecutions : Optional[int]
        The amount of provisioned concurrency requested.
    Status : Optional[Literal['IN_PROGRESS', 'READY', 'FAILED']]
        The status of the allocation process.
    StatusReason : Optional[str]
        For failed allocations, the reason that provisioned concurrency could
        not be allocated.
    """

    AllocatedProvisionedConcurrentExecutions: int | None = None
    AvailableProvisionedConcurrentExecutions: int | None = None
    FunctionArn: str | None = None
    LastModified: str | None = None
    RequestedProvisionedConcurrentExecutions: int | None = None
    Status: Literal["IN_PROGRESS", "READY", "FAILED"] | None = None
    StatusReason: str | None = None
