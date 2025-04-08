from pydantic import BaseModel


class AccountUsage(BaseModel):
    """
    The current usage statistics for an AWS Lambda account.

    Contains information about the number of Lambda functions and the amount
    of storage being used for deployment packages and layer archives.

    Parameters
    ----------
    FunctionCount : Optional[int]
        The number of Lambda functions currently defined in the AWS account.
        This includes all functions regardless of their state (active, inactive, etc.).
    TotalCodeSize : Optional[int]
        The amount of storage space, in bytes, that's being used by deployment packages
        and layer archives across all functions in the account. This represents the
        current consumption against the TotalCodeSize limit.
    """

    FunctionCount: int | None = None
    TotalCodeSize: int | None = None
