from pydantic import BaseModel, Field


class AccountLimit(BaseModel):
    """
    Limits that are related to concurrency and storage in AWS Lambda.

    All file and storage sizes are represented in bytes.

    Parameters
    ----------
    CodeSizeUnzipped : Optional[int]
        The maximum size of a function's deployment package and layers when they're
        extracted.
        This limit applies to the total size of all extracted files and layers.
    CodeSizeZipped : Optional[int]
        The maximum size of a deployment package when it's uploaded directly to Lambda.
        For larger files, Amazon S3 is recommended as an intermediary.
    ConcurrentExecutions : Optional[int]
        The maximum number of simultaneous function executions allowed in the AWS
        account.
        This represents the total concurrent executions limit for all functions in
        the account.
    TotalCodeSize : Optional[int]
        The amount of storage space available for all deployment packages and
        layer archives
        across all functions in the AWS account.
    UnreservedConcurrentExecutions : Optional[int]
        The maximum number of simultaneous function executions, minus the capacity
        reserved for individual functions with PutFunctionConcurrency.
        Must be at least 0.
    """

    CodeSizeUnzipped: int | None = None
    CodeSizeZipped: int | None = None
    ConcurrentExecutions: int | None = None
    TotalCodeSize: int | None = None
    UnreservedConcurrentExecutions: int | None = Field(None, ge=0)
