from typing import Literal

from pydantic import BaseModel, conint, constr


class PutProvisionedConcurrencyConfigRequest(BaseModel):
    """
    Request model for adding a provisioned concurrency configuration to an AWS
    Lambda function's alias or version.

    Attributes
    ----------
    FunctionName : str
        The name or ARN of the Lambda function.
    Qualifier : str
        The version number or alias name.
    ProvisionedConcurrentExecutions : int
        The amount of provisioned concurrency to allocate for the version or alias.
    """

    FunctionName: constr(
        min_length=1,
        max_length=140,
        pattern=r"(arn:(aws[a-zA-Z-]*)?:lambda:)?([a-z]{2}(-gov)?-[a-z]+-\d{1}:)?(\d{12}:)?(function:)?([a-zA-Z0-9-_]+)(:(\$LATEST|[a-zA-Z0-9-_]+))?",  # noqa: E501
    )
    Qualifier: constr(min_length=1, max_length=128, pattern=r"(|[a-zA-Z0-9$_-]+)")
    ProvisionedConcurrentExecutions: conint(ge=1)


class PutProvisionedConcurrencyConfigResponse(BaseModel):
    """
    Response model for adding a provisioned concurrency configuration to an AWS Lambda
    function's alias or version.

    Attributes
    ----------
    AllocatedProvisionedConcurrentExecutions : int
        The amount of provisioned concurrency allocated.
    AvailableProvisionedConcurrentExecutions : int
        The amount of provisioned concurrency available.
    LastModified : str
        The date and time that a user last updated the configuration,
        in ISO 8601 format.
    RequestedProvisionedConcurrentExecutions : int
        The amount of provisioned concurrency requested.
    Status : str
        The status of the allocation process.
    StatusReason : str
        For failed allocations, the reason that provisioned concurrency could not be
        allocated.
    """

    AllocatedProvisionedConcurrentExecutions: conint(ge=0)
    AvailableProvisionedConcurrentExecutions: conint(ge=0)
    LastModified: str
    RequestedProvisionedConcurrentExecutions: conint(ge=1)
    Status: Literal["IN_PROGRESS", "READY", "FAILED"]
    StatusReason: str | None
